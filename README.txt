[INSTALL]

# soft link rc files to git files
> rm ~/.bashrc && ln -s ~/syncfiles/dotfiles/bashrc ~/.bashrc
> rm ~/.screenrc && ln -s ~/syncfiles/dotfiles/screenrc ~/.screenrc
> rm ~/.vimrc && ln -s ~/syncfiles/dotfiles/vimrc ~/.vimrc

# pathogen (ttps://github.com/tpope/vim-pathogen)
> mkdir -p ~/.vim/autoload ~/.vim/bundle
> curl -Sso ~/.vim/autoload/pathogen.vim https://raw.github.com/tpope/vim-pathogen/master/autoload/pathogen.vim

# NERDtree (https://github.com/scrooloose/nerdtree)
> cd ~/.vim/bundle
> git clone https://github.com/scrooloose/nerdtree.git

# Toggle plugin
> mkdir -p ~/.vim/plugin
> wget http://www.vim.org/scripts/download_script.php?src_id=13834 -O toggle.vim
> cp toggle.vim ~/.vim/plugin && rm toggle.vim


