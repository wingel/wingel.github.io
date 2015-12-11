---
layout: post
title: Getting the HTML source from an Android WebView
date: '2014-03-05T01:40:00.000+01:00'
tags:
modified_time: '2014-03-05T02:01:05.255+01:00'
id: tag:blogger.com,1999:blog-4618495377058807667.post-2915903775355369815
redirect_from: /2014/03/getting-html-source-from-android-webview.html
---

On and off I'm working on writing an [Atom/RSS feed
reader](http://blog.weinigel.se/2013/10/weader-simple-atomrss-feed-reader-for.html)
for Android. The feed reader is using an Android WebView to display
the contents of a feed and to be able to debug some issues I had I
wanted to be able to view the HTML source for a page.

  
That's should be simple I though, just do WebView.getData() and show
it in a dialog. But no, there's no method to get the HTML source from
a WebView, so one has to jump through a [lot of
hoops](http://lexandera.com/2009/01 /extracting-html-from-a-webview/)
to do that. Also the examples I found uses
WebView.addJavaScriptInterface to do its job which is not such a good
idea because addJavaScriptInterface has [security
problems](http://blogs.avg.com/mobile/analyzing-android-webview-exploit/)
and [doesn't even work on Android
2.3](http://www.jasonshah.com/handling-android-2-3-webviews-broken-addjavascriptinterface/). And
I do want my application to run on fairly old Android devices (I still
use a Motorola Defy at work, I like the form factor and that it's
waterproof).

So after a bit of thinking I figured out an easier way of getting the
source.  There is a class called WebViewClient which among other
things can be used to override what should happen when a follows a
link in the WebView. This together with a bit of JavaScript can be
used to get the source.

First, when initializing the WebView, tell it to use a custom
WebViewClient:

     mWebView = (WebView) mView.findViewById(R.id.web);
     mWebView.setWebViewClient(new MyWebViewClient());

When asked to view the source, enable JavaScript for the WebView and
then inject a bit of JavaScript which builds and follows an URL
containing the HTML:

     public void viewSource() {
       mWebView.getSettings().setJavaScriptEnabled(true);
       mWebView.loadUrl(
         "javascript:this.document.location.href = 'source://' + encodeURI(document.documentElement.outerHTML);");
     }

The custom WebViewClient will catch this URL:

     public class MyWebViewClient extends WebViewClient {
         public boolean shouldOverrideUrlLoading(WebView view, String url) {
             if (url.startsWith("source://")) {
                 try {
                     String html = URLDecoder.decode(url, "UTF-8").substring(9);
                     sourceReceived(html);
                 } catch (UnsupportedEncodingException e) {
                     Log.e("example", "failed to decode source", e);
                 }
                 mWebView.getSettings().setJavaScriptEnabled(false);
                 return true;
             }
             // For all other links, let the WebView do it's normal thing
             return false;
       }
     }

And we can finally show the source in a dialog:

     private void sourceReceived(String html) {
       AlertDialog.Builder builder = new AlertDialog.Builder(this);
       builder.setMessage(html);
       builder.setTitle("View Source");
       AlertDialog dialog = builder.create();
       dialog.show();
     }

As simple as that. And it seems to work on everything from Android 2.3
up to Android 4.4.

Although what we get from the WebView does not quite seem to be the
source code it was fed to begin with. It seems that the WebView will
fix up the HTML so that it is correct and will also decode any
entitydefs. So for example if the WebView was fed "<p>Hello
W&ouml;rld<p>" what we would get back is
"<html><head></head><body><p>Hello Wörld<p></body></html>". It's still
useful for what I wanted to do though.
