---
layout: post
title: Emacs and python.el
tags:
- nerdy stuff
- emacs
- python.el
- scratching an itch
excerpt:
id: 0af90553-a3d6-4f46-ab6a-3e788f71f518
---

I use Emacs for most of my programming.  I do a lot of programming in
Python.  So quite naturally I use Emacs for a lot of Python programming.

I started using python-mode.el a long time ago and have desperately
clung to it since then.  I just do not like how the newfangled
python.el does things at all.

If I understand correctly, the idea with python.el is that you start a
long running Python process with C-c C-p (run-python) and then
incrementally feed it with snippets of code using C-c C-c
(python-shell-send-buffer) or C-c C-(r python-shell-send-region).


I don't like this.  This is not how I want to do things.  If I run the
following code multiple times with C-c C-c, x is going to increment:

    if 'x' not in locals():
        x = 0
    x += 1
    print("x", x)

State stays between runs.  If I do:

    import module

and modify module.py, those changes won't be picked up again unless I
kill the long running process and start it again.  Or I reload the
module by hand, but that quickly becomes unworkable if the module is
used in multiple places.  When I press C-c C-c to run my Python code I
want to start from a clean predictable slate.  I want a new fresh
instance of Python running in an empty buffer every time.  This way I
will know that there isn't any state left over from previous runs.

And, as a nice surprise, python.el silently strips out any code inside
a block like this:

    if __name__ == '__main__':
        main()

That made me quite confused the first time I tried to run a Python
program from within Emacs and nothing happened.  I ended up running it
from the command line instead.  When I got frustrated enough I started
digging into it and figured out what had happened.  I decided that
python.el was crap and went back to python-mode.el again.

But now I have a machine with a new shiny Emacs 25 on it and my old
trust python-mode.el finally broke in such a way that I couldn't fix
it.  I really don't do lisp; I've never gotten into the language, so
my "lisp programming sessions" usually consist of reading what other
people on the internet have done and copying snippets into my .emacs.

But this time I was frustrated enough so that I actually did something
about this and managed to hack together a function,
run-python-classic, which I have mapped to it C-c C-c so that Emacs
runs Python code from a buffer the way I want it to.

As a small bonus I also added some code to parse any #! at the top of
the file to figure out which Python interpreter to run.  So if I have
a file with the following line at the top:

    #! /usr/bin/python3

C-c C-c will now use that information and start that version of
Python.  Very convenient when switching between maintaining old
Python&nbsp;2 code and new Python&nbsp;3 code.

One small itch scratched.  Now I just have to figure out what I was
trying to actually write in Python before getting sidetracked.

    ;; Parse any #! line at the top of the file to figure out what
    ;; interpreter to use
    (defun get-script-interpreter ()
      (interactive)
      (let ((l (save-excursion
                 (goto-char (point-min))
                 (setq s (point))
                 (move-end-of-line 1)
                 (setq e (point))
                 (buffer-substring-no-properties s e))))
        (if (string-match "^\#![ \t]*\\(.*\\)" l)
            (match-string 1 l))
        )
      )

    ;; Run Python in a classic way like old python-mode.el used to do.

    (defun run-python-classic ()
      "Run the python code in the current buffer in a new Python process."
      (interactive)

      ;; Kill any existing python process
      (ignore-errors (delete-process (python-shell-get-process)))

      ;; Erase an existing *Python* buffer or create a new one.
      ;; Make it visible and switch focus to it.
      (save-current-buffer
       (set-buffer (get-buffer-create "*Python*"))
       (let ((inhibit-read-only t)) (erase-buffer))
       (display-buffer (current-buffer))
       (switch-to-buffer-other-frame (current-buffer))
       )

      ;; If there is a #! line at the beginning of the buffer use it as
      ;; the command to start the interpreter.  If not, pass nil and use
      ;; the default interpreter
      (let ((cmd (get-script-interpreter)))
        (run-python cmd))

      ;; Since there shouldn't be any long lived data in the *Python*
      ;; buffer buffer, don't ask for confirmation when killing it.
      (set-process-query-on-exit-flag (python-shell-get-process) nil)

      ;; Finally send the buffer contents to the process and bypass the
      ;; code that strips out if __name__ == '__main__'.
      (save-restriction
        (widen)
        (let* ((process (python-shell-get-process))
               (string (buffer-substring-no-properties (point-min) (point-max))))
          (python-shell-send-string string process)
          )
        )
      )

    ;; This doesn't play well with the interpreter stuff, so disable it
    (setq python-shell-completion-native-enable nil)

    ;; Finally add a hook to replace C-c C-c with the classic variant
    (defun my-python-mode ()
      (setq py-indent-offset 4)
        (setq indent-tabs-mode nil)
          (define-key python-mode-map "\C-c\C-c" 'run-python-classic)
            )

    (add-hook 'python-mode-hook 'my-python-mode)
