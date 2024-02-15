---
layout: post
title: Help! I'm on the Command Line!
date: '2023-05-08 07:00:23'
tags:
- linux
- command line
---

You’re administering a \*nix server somewhere, playing with the settings, and now that you’ve figured out how to ssh into the stupid box you’re greeted with a friendly `you@server:~$` and a blinking cursor. “Great, now what?” you ask. Well, that’s why I’m here.

* * *

The command prompt

OK, you’re looking at this cryptic line, known as the variable PS1. Interesting, yes? No? Ok, no not really. This is usually set like I’ve outlined above, but what does it mean? Let’s break it down. `you` is the username that you’re currently logged in as. `@server` is the name of the machine where you’re logged in. `~` is the folder you’re actively looking at. `$` is just a separator between that information and the stuff you’re about to type. The PS1 variable is customizable, and some systems will just have a `#` with nothing, while others have a huge string of (hopefully) useful information embedded in the prompt line. Search for "custom ps1" if you’re interested in customizing that rabbit hole.

## **The Filesystem**

The linux filesystem is…well… a little crazy, from a [certain point of view](https://youtu.be/2nO0uJenOgw?t=47). If you’re used to finding C: or A: in a Windows filesystem, and everything is stuck in folders where everything is contained in the same folder, you’re in for a shock. It’s a bit like switching from the [Dewey Decimal System](https://en.wikipedia.org/wiki/Dewey_Decimal_Classification) to the [Library of Congress Card Catalog](https://en.wikipedia.org/wiki/Library_of_Congress_Classification). Both catalog books, but one is more widely seen by the public, so the switch can be painful. It’s not that either is necessarily the “right” way, it’s just different. Tomaeto/tomahto, etc.

### **/**

We’re mostly dealing with tradition here, so bear with me. Back in ‘76 when Unix on the PDP-11 was the best you could hope for, 10 characters-per-minute appearing on the screen was blazing fast. As a result, shorthand was used for _everything_. So the root of the filesystem was just a slash, `/`. No drive letter, nothing. You’ll see that these short commands are nearly always the oldest, just for that reason. Given that the rest is mostly convention, `/` is the only truly guaranteed location on a \*nix system. Luckily, it’s super unusual to find something that deviates from the norm, I mean it’s been nearly 50 years since it was invented, right?

### **/etc**

This folder is for your configuration files. This is most likely where you’ll be mucking about with a server. `/etc/fstab` is the filesystem table, where disks and such are mounted. “Mounted?!” You say? Well, on every system, even if it doesn’t say, there can be a disk or filesystem that is detected, but not necessarily available to the system. Once it’s mounted, that’s when you can actually do stuff to the data that’s stored there. the fstab is what does that automatically on boot. There’s loads of configurations, and depending on your system you might have to hunt a bit to find where to look. `/etc` gives you a start.

### **/var**

Looking for your logs without a forest? They’re here! `/var/log` is going to be your friend if you’re log hunting, this is where you need to look. There’s also an internal mail, print spool, and temporary file directory.

### **/usr**

[Yoooozrrrzzz](https://youtu.be/DkTb7Pe2MtY?t=136)… Yup this is the place where all the user-level files are located. `/usr/bin` is a nice place to look if you’re wanting to find out which programs are installed, but otherwise is going to be left alone.

### **/home**

This is where all the user-land files are. All your precious cat pictures, skateboard-fails, and defunct wordstar files reside here. If you’re going to back up only one thing, let it be `/home`.

### **/srv or /http**

Here’s your server files, and all the web pages you have on this thing. Apache or Nginx serverblock files are here, and this is where you’ll need to go if your pages aren’t loading.

## **Navigating the filesystem: cd and ls**

### **CD, not your obsolete physical audio format**

Remember when I said the shortest commands are the oldest? Well here they come. First, you’re going to need a way to move around. This is done with the “Change Directory” command, `cd`. But where to go? If you just type `cd` and `&lt;enter&gt;`, you’ll go to your home directory, located at `/home/you/`. This is represented by a tilde, `~`. Figuratively, as you go further from the root directory, this is considered “down”. So “up” one level is represented by two periods, `..`. So now you can get to `/home` with `cd ..`. But how do you know what’s there?

### **ls**

The list function, `ls` is pretty handy, as it’s the only way you know what’s in the directory you’re in. This is where we get into something called a switch. It’s just a modifier to change the way a program acts. By default, `ls` will list all the visible files in a multi-column format. But say you want to see more detailed information? Just add `-l` to the end of the line and see what happens. Whoa! All in a single line, with a huge amount of detail. Now try `-a`. Back to the same old boring column format, but with a bunch more files added. That is the “list all” switch, which doesn’t hide stuff starting with a dot, which are hidden files or directories. Many of the configuration options are in hidden files, so don’t forget to look. Switches can be nested, so `ls -la` will list all the files in detailed format.

### **man**

OK, before we go any further, let’s get into the “man” pages. No, it’s not a chauvinistic website, it’s the command-line manual. Try `man ls` to learn some more switches for ls. The arrow keys work for up and down, and `q` quits out of it. Almost all commands have a man page, which is super useful as a reference, but not as a standalone manual since you really need to know what you’re looking for to be able to use it. A very useful place to start is to read the man page for man, `man man`.

## **Looking at text: cat, less, head and tail**

### **[cat](https://youtu.be/JxS5E-kZc2s): not just for youtube videos**

Now that you’ve found your log file, how in the world do you get to see it? Just type `cat` and then your desired file. If the file you wanted to look at was relatively small, it’ll show up all on the screen. Otherwise, it’ll scroll the entire file as fast as it can render until it reaches the end. In that case, keep reading.

### **less is more**

In the very likely event that you’ve got a file which is longer than your screen size, the `less` program will help you immensely. `less *filename*` will bring up a screen which will allow you to scroll back and forth in the window with the arrow keys (unlike the program `more`, which doesn't allow scrolling backwards). Pressing `h` will bring up the help screen, which has a lot of options.

### **When you only need a little: head and tail**

In addition to less, there are two programs which can make quick work of the latest changes to a file: `head` and `tail`. As their name implies, they will strip the start or end of a file and print the results to the console. Either program will take a `-n` switch, followed by a number which will tell it how many lines to print. The default is 10 lines.

### **Pipe to GREP for some geeky searching**
OK, put on your suspenders and get out the Cheetos, we’re going to grok the grep. Grep, the GNU Regular Expression Parser, is a neat little program which will, at it’s most basic, spit out the results of a matching expression to the console. It uses regular expressions, which can be quite complex but very useful when searching. Ever wonder what the sign above the backslash symbol (|) does? Well, other than making some mad [ASCII art](https://www.asciiart.eu/animals/cats), it’s called a pipe, and it’s pretty neat. Say you’ve got a 300mb text file called rayneboughs, and you’re looking for every occurrence of the word gnunicorn. You would be able to push the text of that file to the console with `cat`, right? Well, if you have a pipe after that, it will push that output to the start of the next program instead. This is the foundation of “one-liners”, little scripts which do powerful things like this:

`cat rayneboughs | grep gnunicorn`

This little bit will output every line in the file rayneboughs which contains the word gnunicorn. Cool, huh? Grep is very powerful, and nearly it’s own scripting language, well worth the time to research a bit more to get into the power of regular expressions.

The same function can be had by typing `grep gnunicorn rayneboughs`, but this is a good way to get familiar with pipes, as they can be super handy. For example, piping can alleviate some of the headaches with individual switches, and keep your structure more readable.

## **Editing text: vi, vim, emacs, nano, ad infinitum**

While viewing text files is all well and good, it’s time to actually change something. Some of the things we’ve covered can actually change files, but if you’re going to get to work on your configurations, it’s time to step into the middle of the [holy war](http://en.wikipedia.org/wiki/Editor_war) that is console text editing.

### **vi/vim**

The first of the text editors I’m bringing up is vi, the most universally installed text editor on linux systems. Originally envisioned by Bill Joy in 1976, it’s currently maintained by Bram Moolenaar and is likely to be installed by default on every machine in the 'verse regardless of the distribution you’re running. For that reason alone, you need to at least be familiar with how to modify, save, and close a file. That said, my first several attempts at learning vi nearly resulted in a [manual override](https://youtu.be/YZkC26-3t6U) on the machine. Typing vi on most machines will bring up Vi iMproved, known as Vim, which has the nicety of a status bar at the bottom which tells you which mode you’re in. Yeah, mode. You see, every key can do something different depending on which mode you’re in. There’s “normal” mode, which is the default state of the program (and also the result of much anguish), and “insert” mode, which is what you _normally_ think of when you’re writing text. There’s also “visual” mode, but we’re not going to worry about that for the moment.

Upon opening a vim session with no file, you’re greeted by the default screen with a couple shortcuts which tell you very little. “type :q to quit” looks a bit cryptic, but it means what it says. The colon character “:” is the normal mode command line character, and is how you do file operations. Here’s the basics:

Normal Mode:

`j` Down

`k` Up

`h` Left

`l` Right

_Note: the movement keys work in all versions of vim, including vi. Sometimes the arrow keys will result in funny character displays, so you might have to default to these_

`i` switch to insert mode, will begin inserting characters before the cursor

`a` switch to insert mode, inserting characters after the cursor

`:w` save file

`:q`quit program

`:wq`save and quit

`:q!` quit, discard changes

While in insert mode, press `esc` &nbsp;to switch back to normal mode.

While there’s much more to all of these editors, I’ll leave it up to you to see if you want to dive deeper and become a text ninja.

### **emacs**

Sometimes described as it’s own operating system, emacs was developed in 1976 by Richard Stallman and Guy Steele. It makes excessive use of the `ctl` and `alt` (Modifier) keys to switch in and out of modes. There’s support for a couple of games, an email client, internal compilers, and a host of other things. It might be a bit much for changing a config file, but if it’s what’s installed, you might as well jump in.

Moving around is a matter of forward and backward one character at a time, or next and previous one line at a time. Text can be inserted at any time, once you’ve gotten the cursor there.

Save the file by pressing ` s`

There is an integrated help, loaded by pressing ` i`.

To exit, press `,`

This should be enough to get a file edited and saved, for more information the program is quite well documented internally with the help function.

### **nano/pico**

While the original PIne COmposer, PICO, appears to have been abandoned with it's original mail client, the University of Washington's PINE client, it’s successor, nano, is alive and well. Nano is likely to be the go-to editor of choice for the occasional command-line user, as it’s got a helpful menu bar at the bottom and is not modal. It uses some of the previously mentioned control commands from emacs, but those aren’t required for moving around and making changes. The backspace and arrow keys work fine, and generally there’s no surprises.

### **Others**

There are hosts of other editors, such as jed, sanos, cream, elvis, and more, but the general rule is: if you don’t like your editor, install another one!

### **But that’s not all!**

We’ve only scratched the surface of the power of the command line, but this should be enough to get you through the first few times of command-line goodness enough to get you familiar with the workflow. Do not be afraid! Next up: processes, multiplexers and scripts, oh my!

