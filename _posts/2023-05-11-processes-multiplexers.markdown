---
layout: post
title: Processes, multiplexers and scripts, oh my!
date: '2023-05-11 13:36:03'
tags:
- linux
- command line
---

# 

# Processes

Now that we have an understanding of how to do some basic text editing on the command line, lets get down into some of the running processes of your system.

* * *

#### Uptime

OK, now that we’ve got a reasonable handle on moving around the file structure, let’s find out what’s going on in the system. For starters, let’s find out how long the system’s been running and how hard by typing `uptime`. This will give a wonderfully cryptic output looking something like this: `20:49:35 up 12:21, 1 user, load average: 0.39, 0.76, 1.00` Sure…whatever. Here it is broken down:

Output   Meaning

`20:49:35` The current time

`up 12:21` How long this system has been running without a reboot, in D:H:M format.

`1 user`  Obviously, how many users are logged in

`load average: 0.39, 0.76, 1.00`

OK, here’s where we get sticky.

Let’s break this part a little further.

“Load average” is a metric of the amount of work currently being handled by the system, including CPU, RAM, and disk. This is expressed as a number corresponding to percent utilization divided by 100. So a 1.00 load is using 100% of the available resources of your machine. A number above 1 means that there are processes waiting in line to be calculated by the CPU, and a number below 1 means that the system is idling part of the time. Why three numbers? Well, these are the averages for the past minute, 5 minutes, and 15 minutes respectively.

#### Top

Now that we have an idea of how the system’s doing, let’s find out exactly what’s running. `top` will give a nice list of all the running processes. Does that first line look familiar? Yup, that’s the output of `uptime`. It self-updates every couple of seconds, so if you’re system is really bogged down `top` might not be your first choice, but it’s nice to see all the running processes.

#### ps

Back to two-letter commands, ps is the process snapshot utility. There’s a bunch of switches, but the easiest way to list all the current relevent processes is `ps aux`. This will usually output lots of info, so you can manually look at it by piping to less, (`| less`) or search the output with `grep` if you know what you’re looking for. If you’re just looking for the maximum process, try this: `ps aux|sort -k 3n` This uses another nice tool, `sort`, which does exactly what it says, it sorts. the `-k 3n` is it’s switch to tell it to sort by the third column, sorting numerically.

### Multiplexers: Screen and Tmux

Sometimes you want to leave something running after you log out, such as a backup script. But all the processes associated with your login are terminated when you log out, so how are you to cope? A “terminal multiplexer” is what you want. Let’s look at a couple. `C` is short for `ctrl` in this next section:

#### Screen

Screen is often installed on remote systems, if for no other reason that if you are disconnected, your session is just detached and you can just log in and resume your work from where you left off. `screen` will bring up something that looks…exactly like what you just had. Huh. This is actually not true, it’s a “virtual” terminal. If you type `<C-a>, d`, you will detach from the session and leave anything running that was previously running. `<C-a>, k` kills the window, while `screen -r` will reattach the session. Cool, huh? You can do all sorts of things with a multiplexer, such as split the screen and run a bunch of things at once.

Keystroke

Action

`<C-a> S`

Split horizontally

`<C-a> |`

Split vertically

`<C-a> <tab>`

Switch to next pane

#### Tmux

Tmux, or “terminal multiplexer” is kind of the vim to screen’s vi. It has a status bar, which is quite helpful, as well as an easy way to customize the keyboard shortcuts so they’re easy to remember. The defaults are as follows:

Keystroke

Action

`<C-b> &`

Kill window

`<C-b> %`

Split vertically

`<C-b> "`

Split horizontally

`<C-b> o`

Switch to next pane

`<C-b> d`

Detach session

`tmux attach`

Attach a previously detached session

### Scripting

Now that we’ve gotten some commands under our belts, it’s time to write a script. Open up an editor, and put this in the first line: `#!/bin/bash` This tells the system which program to use to run the next lines. Now on the second line, just put `ls`. Save the file as a `.sh` file, and change the file permissions to be able to execute with `sudo chmod +x filename`. the `sudo` command allows you to be root for a single command instead of logging in as root, which is helpful for security and generally not screwing things up. Run your file by typing `sh filename.sh`. You’re now looking at the output of the `ls` command, right? While this is not actually a useful thing to write a script for, it illustrates the point of bash scripts: anything you can type on the command line can be in a script. Let that sink in a bit. Do you have a huge one-liner that you can’t ever remember? Try putting it in a script instead of writing it on a post-it. Bash scripts can use if-then loops, case statements, and take input from the user to become a very flexible and powerful way of managing systems. There are lots of books and tutorials on the subject, so I’m not going to attempt to repeat their fine work. Go, read, and enjoy.

### Final Thoughts

While this is not by any means a complete course in command-line use, I hope it’s gotten you on your way to be able to start to learn for yourself how powerful this method of computing can be. It’s not pretty, I grant you. But it’s low-bandwidth and very powerful once you get over the learning curve. Here’s a parting shot: Have a bunch of programs that you need to install on a fresh Debian-based system? Try this one, after putting each program on it’s own line in a plain text file called `programs`:

`cat programs| xargs sudo apt-get install`

`BOOM!`

