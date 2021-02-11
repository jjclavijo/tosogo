#!/bin/bash

# Add local user
# Either use the LOCAL_USER_ID if passed in at runtime or
# fallback
# DOCS: https://denibertovic.com/posts/handling-permissions-with-docker-volumes/

USER_ID=${LOCAL_USER_ID:-9001}

echo "Starting with UID : $USER_ID"
useradd --shell /bin/bash -u $USER_ID -o -c "" -m user
export HOME=/home/user

cd $HOME

chown -R user /opt/venv
chown -R user /rtklib

#cp -r /pytmp .

#chown -R user pytmp
#cd pytmp
# /usr/local/bin/gosu user pip -- install flit
#/usr/local/bin/gosu user python -m flit install -s

# Dummy cleanup

function cleanup(){
  echo "no cleaning needed"
}

if [ $PROY_HOME = "/proyecto" ]
then
  cd $PROY_HOME
  if [ $(stat --format '%u' ".") = 0 ]; then
    echo Using internal PROY_HOME
    chown -R $USER_ID:$USER_ID .
  elif [ $(stat --format '%u' ".") = $USER_ID ]; then
      echo Using same-user mounted PROY_HOME
  else
      orig_user=$(stat --format '%u' ".")
      echo Using othed-user mounted PROY_HOME
      chown -R $USER_ID:$USER_ID .

      function cleanup () {
        echo "restoring permissions"
        chown -R $orig_user:$orig_user "$PROY_HOME"
      }

  fi
fi

# if user mounted a notebooks volume work there
if [ -d /notebooks ]
then  
  cd /notebooks
  if [ $(stat --format '%u' ".") = 0 ]; then
    echo Using internal notebook_dir
    chown -R $USER_ID:$USER_ID .
  elif [ $(stat --format '%u' ".") = $USER_ID ]; then
      echo Using same-user mounted PROY_HOME
  else
      orig_user=$(stat --format '%u' ".")
      echo Using othed-user mounted PROY_HOME
      chown -R $USER_ID:$USER_ID .

      function cleanup () {
        echo "restoring permissions"
        chown -R $orig_user:$orig_user "$PROY_HOME"
      }

  fi
else
  mkdir /notebooks 
  chown -R user /notebooks
  cd /notebooks
fi

/usr/local/bin/gosu user "$@" &

cmdpid=$!

function realclean() {
  echo "Closing mainpid"
  kill -TERM $cmdpid
  echo "Cleaning"
  cleanup
  exit
}

function killandclean() {
  echo "Killing mainpid"
  kill -KILL $cmdpid
  echo "Cleaning"
  cleanup
  exit
}

trap realclean SIGTERM;
trap realclean SIGINT;
trap killandclean SIGKILL;

wait $!

cleanup
