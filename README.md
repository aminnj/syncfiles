# miscfiles
Contains:
* Patched Droid Sans Mono font with Powerline symbols and smooth box/line drawing characters for use in tmux (used fontforge to do this). Looks much nicer than the officially offered patched version of the font for powerline.
** https://github.com/todylu/monaco.ttf **
* ROOT macro to open TBrowser: `tb` or `tb test.root`
* ROOT macro to print number of events in ROOT files: `nevts test.root` or if they are in a folder, `nevts path/to/folder/`
* USA script to print the flag, because every terminal needs more 'Murica: `usa`
* Script to take folder with pdfs inside and convert each pdf to png, create an index file, and upload to website: `package foldername`
* Script to add numbers to pdf file: `addnumbers test.pdf` or `addnumbers test.pdf --wide`
* Script to convert ROOT histogram (printed to tex) into pdf


# INSTALL

## get Wombat color scheme
> mkdir -p ~/.vim/colors && cd ~/.vim/colors && wget -O wombat256mod.vim http://www.vim.org/scripts/download_script.php?src_id=13400

## soft link rc files to git files
> rm ~/.bashrc && ln -s ~/syncfiles/dotfiles/bashrc ~/.bashrc
> rm ~/.screenrc && ln -s ~/syncfiles/dotfiles/screenrc ~/.screenrc
> rm ~/.vimrc && ln -s ~/syncfiles/dotfiles/vimrc ~/.vimrc
> rm ~/.tmux.conf && ln -s ~/syncfiles/dotfiles/tmuxrc ~/.tmux.conf

## pathogen (https://github.com/tpope/vim-pathogen)
> mkdir -p ~/.vim/autoload ~/.vim/bundle
> curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim

## NERDtree (https://github.com/scrooloose/nerdtree)
> cd ~/.vim/bundle
> git clone https://github.com/scrooloose/nerdtree.git

## syntastic (https://github.com/scrooloose/syntastic)
> cd ~/.vim/bundle
> git clone https://github.com/scrooloose/syntastic.git

## vim-commentary (https://github.com/tpope/vim-commentary)
> cd ~/.vim/bundle
> git clone git://github.com/tpope/vim-commentary.git

## vim-surround (https://github.com/tpope/vim-surround)
> cd ~/.vim/bundle
> git clone git://github.com/tpope/vim-surround.git

## supertab (git clone https://github.com/ervandew/supertab)
> cd ~/.vim/bundle
> git clone https://github.com/ervandew/supertab

## tagbar (git clone https://github.com/majutsushi/tagbar.git)
> cd ~/.vim/bundle
> git clone https://github.com/majutsushi/tagbar.git



## Toggle plugin
> mkdir -p ~/.vim/plugin
> wget http://www.vim.org/scripts/download_script.php?src_id=13834 -O toggle.vim
> cp toggle.vim ~/.vim/plugin && rm toggle.vim

# COPY & PASTE
``` bash
mkdir -p ~/.vim/colors && cd ~/.vim/colors && wget -O wombat256mod.vim http://www.vim.org/scripts/download_script.php?src_id=13400
xrdb -merge ~/.Xresources
mkdir -p ~/.vim/autoload ~/.vim/bundle
curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim
cd ~/.vim/bundle
git clone https://github.com/scrooloose/nerdtree.git
git clone https://github.com/scrooloose/syntastic.git
git clone git://github.com/tpope/vim-commentary.git
git clone git://github.com/tpope/vim-surround.git
git clone https://github.com/ervandew/supertab
git clone https://github.com/majutsushi/tagbar.git
mkdir -p ~/.vim/plugin
wget http://www.vim.org/scripts/download_script.php?src_id=13834 -O toggle.vim
cp toggle.vim ~/.vim/plugin && rm toggle.vim

rm -f ~/.bashrc && ln -s ~/syncfiles/dotfiles/bashrc ~/.bashrc
rm -f ~/.screenrc && ln -s ~/syncfiles/dotfiles/screenrc ~/.screenrc
rm -f ~/.vimrc && ln -s ~/syncfiles/dotfiles/vimrc ~/.vimrc
rm -f ~/.Xresources && ln -s ~/syncfiles/dotfiles/Xresources ~/.Xresources
rm -f ~/.tmux.conf && ln -s ~/syncfiles/dotfiles/tmuxrc ~/.tmux.conf
```

# PYFILES
## miscutils.py
Contains various functions that would find common use in python. My hack for allowing importing of miscutils would be:
``` python
import sys, os
sys.path.append(os.getenv("HOME") + '~/syncfiles/pyfiles')
```
or we can modify the pythonpath variable for this (included in bashrc)

## stats.py
Takes piped input and prints out length, mean, sigma, sum, min, max. It can ignore non-numerical lines, but it only handles 1 column. If specified, the first argument of stats.py provides the column of piped input to use
``` bash
seq 1 1 10 | stats
```
produces
```
        length: 10
        mean:   5.5
        sigma:  3.0276503541
        sum:    55.0
        min:    1.0
        max:    10.0
```
Additionally, if no numbers are detected, but a few text objects are found, it will output a frequency histogram of the text (column specification also works for this).
``` bash
ls -l | stats 6
```
produces
```
Found 36 words, so histo will be made!
Apr | ********* (9)
Mar | ******** (8)
Feb | ***** (5)
Aug | **** (4)
May | **** (4)
Jun | ** (2)
Jul | ** (2)
Dec | ** (2)
```

## histo.py
Uses the dumb terminal setting in gnuplot to display a text histogram of the piped data. Currently does not allow column specification, so that must be provided before piping. This requires a single argument of the binwidth

``` bash
# independently sampling a uniform random number 4 times and summing gives something 
# close to a gaussian by the (beautiful) central limit theorem!
for i in {1..10000}; do echo $(( (RANDOM+RANDOM+RANDOM+RANDOM)/4 )); done | histo 2000
```
produces
```
  1800 ++---------+-----------+----------+----------+-----------+---------++
       +          +           +  "-" using (bin($1,binwidth)):(1.0) ****** +
  1600 ++                                ******                           ++
       |                            ******    *                            |
  1400 ++                           *    *    *****                       ++
       |                        *****    *    *   *                        |
  1200 ++                       *   *    *    *   *                       ++
       |                        *   *    *    *   *                        |
  1000 ++                       *   *    *    *   ******                  ++
       |                        *   *    *    *   *    *                   |
       |                   ******   *    *    *   *    *                   |
   800 ++                  *    *   *    *    *   *    *                  ++
       |                   *    *   *    *    *   *    *****               |
   600 ++              *****    *   *    *    *   *    *   *              ++
       |               *   *    *   *    *    *   *    *   *               |
   400 ++              *   *    *   *    *    *   *    *   ******         ++
       |          ******   *    *   *    *    *   *    *   *    *          |
   200 ++         *    *   *    *   *    *    *   *    *   *    *         ++
       +      *****    *   *  + *   *    *    *   * +  *   *    *****      +
     0 ++*******************************************************************
       0         5000       10000      15000      20000       25000      30000
```

# TIPS & TRICKS
You can pipe into vim with "vim -" which reads from STDIN.
```
seq 1 100 | vim -
```

Cut and paste current command with `<Ctrl-U>` and `<Ctrl-Y>`, respectively. So if you type `ls some/long/dir/path/`, but want to `ls` the current directory, you can do `<Ctrl-U>` to yank `ls some/long/dir/path/`, do `ls`, and then `<Ctrl-Y>` to bring back `ls some/long/dir/path/`.

# MISC INSTRUCTIONS
## INSTALLING MATPLOTLIB
download 
freetype-2.4.0.tar.gz   12-Jul-2010 20:17   1.8M     
from
http://download.savannah.gnu.org/releases/freetype/

and

http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-1.3.1/matplotlib-1.3.1.tar.gz/download?use_mirror=iweb

```
install all make+automake+gcc+g++ packages in cygwin
install all freetype-related packages in cygwin
```

unpack freetype and go inside
```
./configure
make
make install
```

unpack and go inside matplotlib
apply this patch to files inside lib/matplotlib/tri/: https://github.com/ianthomas23/matplotlib/commit/1215f78874127c27505616fcd73043991035dd7e

```
python setup.py build
python setup.py install
```

badabing DONE

