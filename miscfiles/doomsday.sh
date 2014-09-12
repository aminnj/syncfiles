#!/bin/bash --posix

################################################################
#                                                              #
#  doomsday.sh                                                 #
#                                                              #
#  A script to help you practise your application of the       #
#  Doomsday algorithm, invented by John Horton Conway.         #
#                                                              #
#      http://en.wikipedia.org/wiki/Doomsday_rule              #
#                                                              #
#  Written by matthew.gilliard@gmail.com, Jan 2011, and        #
#  distributed under the terms of the GNU Lesser General       #
#  Public License: http://www.gnu.org/licenses/lgpl.html       #
#                                                              #
#  For usage info run "doomsday.sh -h"                         #
#   from https://code.google.com/p/doomsday-sh/                #
#          Minor changes by me (Nick)                          #
################################################################

CURRENT_CENTURY=false;
CURRENT_YEAR=false;
SHOW_TIMINGS=false;
FORCE_RETRY=false;
DEBUG=false;
TRAP_CTRL_C=false;

ATTEMPTS=0;

function init {
  while getopts "yctrhkd" option
  do
    case "$option" in
      y)  CURRENT_YEAR=true;;
      c)  CURRENT_CENTURY=true;;
      t)  SHOW_TIMINGS=true;;
      r)  FORCE_RETRY=true;;
      d)  DEBUG=true;;
      k)  TRAP_CTRL_C=true;;
      \?) print_usage_and_exit;;
      h)  print_usage_and_exit;;
    esac
  done

  if $TRAP_CTRL_C; then
    trap '' 1 2 3 6;
  fi

  build_days;
  do_doomsday;

}

function print_usage_and_exit {
  echo "Usage: doomsday.sh -c -y -t -r -k -h";
  echo "  -c restricts the date to the current century";
  echo "  -y restricts the date to the current year";
  echo "  -t prints timing statistics";
  echo "  -r forces you to retry until you get it right";
  echo "  -k \"unkillable\" (prevents ctrl-c)";
  echo "  -h print this information and exit";
  exit 0;
}

function build_days {

  # 01/03/2011 (3rd Jan 2011) was a Monday - use this fact to build a list
  # of the days' names in the current locale

  # quick checks show that this works even if the locale is not set to en_*
  DAY0=$(date +%A -d "03 Jan 2011");
  DAY1=$(date +%A -d "04 Jan 2011");
  DAY2=$(date +%A -d "05 Jan 2011");
  DAY3=$(date +%A -d "06 Jan 2011");
  DAY4=$(date +%A -d "07 Jan 2011");
  DAY5=$(date +%A -d "08 Jan 2011");
  DAY6=$(date +%A -d "09 Jan 2011");

  DAYS="$DAY0 $DAY1 $DAY2 $DAY3 $DAY4 $DAY5 $DAY6";

  debug "Locale is $LANG";
  debug "Days are '$DAYS'";

}

function debug {
  if $DEBUG; then
    echo "DEBUG: $1";
  fi
}

function do_doomsday(){

  choose_date;

  # BASH "time" builtin just writes to stderr.
  # see http://mywiki.wooledge.org/BashFAQ/032
  exec 3>&1 4>&2
  ANSWER_DETAILS=$( 
    { time read_answers "$TARGET_DATE > " $CORRECT_ANSWER 1>&3 2>&4;
      echo $CORRECT;
      echo $ATTEMPTS; } 2>&1 );
  exec 3>&- 4>&-

  # I don't like this much, but...
  TIME_INFO=$( echo $ANSWER_DETAILS | cut -d" " -f 2 );
  CORRECT=$( echo $ANSWER_DETAILS | cut -d" " -f 7 );
  ATTEMPTS=$( echo $ANSWER_DETAILS | cut -d" " -f 8 );

  # If user pressed ctrl-D
  if [ "$CORRECT" == "0" ]; then
    CORRECT=false;
    ATTEMPTS=0;
  fi

  debug "TIME_INFO: $TIME_INFO";
  debug "CORRECT: $CORRECT";
  debug "ATTEMPTS: $ATTEMPTS";

  local EXIT_CODE=1;

  if $CORRECT; then
    echo -ne "\033[1;32m[SUCCESS]\033[0m ($ATTEMPTS attempts)";
    EXIT_CODE=0;
  else
    if [ $ATTEMPTS -eq 7 ]; then
      echo -ne "\033[1;31m[FAILURE]\033[0m 7 wrong guesses!!?! ";
      echo -n  "You are an idiot"; #"ironic" misspelling
    else
      echo -ne "\033[1;31m[ :( ]\033[0m";
    fi
  fi

  if $SHOW_TIMINGS; then
    echo -n " [$TIME_INFO]";
  fi
  echo;

  exit $EXIT_CODE;

}

function choose_date {

  # these years are 1/1/1970 +- 2^32 seconds
  local FROM_YEAR=1902;
  local TILL_YEAR=2038;

  if $CURRENT_CENTURY; then
    FROM_YEAR=2000;
  fi

  if $CURRENT_YEAR; then
    FROM_YEAR=$( date +%Y );
    TILL_YEAR=$(( $FROM_YEAR + 1 ));
  fi

  var1=$RANDOM
  let "var1 %= 2"
  if [ "$var1" -eq 1 ]; then
      FROM_YEAR=2014
      TILL_YEAR=2016
  fi

  local FROM=$( date +%s -d "01/01 $FROM_YEAR" );
  local TILL=$( date +%s -d "01/01 $TILL_YEAR" );

  # might as well use date as an RNG as well
  local RAND=$( date +%N );

  local TARGET_SEC=$(( $FROM + 10#$RAND % ($TILL - $FROM) ));

  TARGET_DATE=$( date +"%B %d %Y" -d "@$TARGET_SEC" );
  CORRECT_ANSWER=$( date +"%A" -d "@$TARGET_SEC" );

}

function read_answers {

  # In a subshell, so trap ctrl-c here, too
  if $TRAP_CTRL_C; then
    trap '' 1 2 3 6;
  fi

  PS3="$1 ";

  # can we make "select" zero-based?
  select answer in $DAYS; do

    (( ATTEMPTS= $ATTEMPTS + 1 ));

    if [ "$answer" == "$2" ]; then
      CORRECT=true;
      return;
    fi

    if [ $ATTEMPTS -eq 7 ]; then
      CORRECT=false;
      return;
    fi

    if ! $FORCE_RETRY; then
      CORRECT=false;
      return;
    fi

  done;

}

#------------------------------------------------------------------------------
# Kick off, passing all script arguments to init

init "$@";
