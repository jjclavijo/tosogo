FROM docker.io/debian:bullseye-slim AS builder

# Install Dependencies and updates

RUN apt-get -y update ; apt-get -y install gfortran gcc make git

RUN mkdir /recipes

# Create unprivileged user for builds
RUN useradd builder -d /recipes;\
    chown -R builder:builder /recipes

# Get RTKLIB pkgfile from AUR
COPY recipes/rtklib /recipes/rtklib

RUN chown -R builder:builder /recipes/rtklib

USER builder

# Install dependencies for build
RUN cd /recipes/rtklib;\
    ./makepkg.sh

USER root

RUN apt-get -y update ; apt-get -y install cmake curl g++ swig python3 libpython3-dev python3-dev python3-setuptools

RUN ln -s $(which python3) $(which python3 | tr -d '3')

# Get RTKLIB pkgfile from AUR
COPY recipes/gpstk /recipes/gpstk

RUN chown -R builder:builder /recipes/gpstk

USER builder

# Install dependencies for build
RUN cd /recipes/gpstk;\
    ./makepkg.sh

USER root

# Copy anubis and gebPP dources
# https://gnutsoftware.com/software/anubis
COPY recipes/anubis /recipes/anubis

RUN chown -R builder:builder /recipes/anubis

# Install dependencies for build
RUN apt-get -y update ; apt-get -y install automake

USER builder

RUN cd /recipes/anubis;\
    ./makepkg.sh

USER root

#https://www.pecny.cz/sw/geb/
COPY recipes/geb-pp /recipes/geb-pp

RUN chown -R builder:builder /recipes/geb-pp

# Install dependencies for build
RUN apt-get -y update ; apt-get -y install libboost-thread-dev libboost-system-dev libboost-filesystem-dev

USER builder

RUN cd /recipes/geb-pp;\
    ./makepkg.sh

USER root

#FROM docker.io/ubuntu:bionic AS glab

# Avoid gLAB, site is down.
# Install Dependencies and updates
#RUN apt update && apt -y --no-install-recommends install build-essential curl
#RUN apt-get install -y --reinstall ca-certificates
#
#COPY recipes/gLAB recipes/gLAB
#
#RUN useradd builder -d /recipes;\
#    chown -R builder:builder /recipes/gLAB
#
#USER builder
#
## Install dependencies for build
#RUN cd /recipes/gLAB;\
#    ./makepkg.sh
#
#USER root

FROM docker.io/debian:bullseye-slim 

RUN mkdir recipes

RUN useradd builder -d /recipes

COPY --from=builder /recipes/rtklib/pkg/* /
COPY --from=builder /recipes/gpstk/pkg/* /
COPY --from=builder /recipes/geb-pp/pkg/* /
COPY --from=builder /recipes/anubis/pkg/* /
#COPY --from=glab /recipes/gLAB/pkg/* /

CMD [ "/bin/bash" ]

#### Get gpstk pkgfile modified from AUR to use version 3.0.0
###COPY /gpstk /builder/gpstk
#### Create unprivileged user for builds
###RUN chown -R builder:builder /builder/gpstk
###
###RUN cd builder/gpstk;\
###    ls ;\
###    source ./PKGBUILD;\
###    pacman -S --noconfirm ${makedepends[@]} ${depends[@]}
###
###RUN cd builder/gpstk;\
###    su builder -c "makepkg -s"
###
###
#### Python virtual environment
###RUN cd opt;\
###    python3 -m venv venv ;\
###    . /opt/venv/bin/activate ;\
###    pip install --no-cache-dir --upgrade pip;\
###    pip install --no-cache-dir jupyterlab ipython pandas numpy matplotlib
###
#### Enable jupyter extension iýwidgets for interactiveness
###RUN . /opt/venv/bin/activate ;\
###    pip --no-cache-dir install ipywidgets jupyter_contrib_nbextensions ipympl;\
###    jupyter contrib nbextension install;\
###    jupyter nbextension enable --py widgetsnbextension
###
#### Install gpstk python swig bindings built alongside package.
###RUN . /opt/venv/bin/activate ;\
###    cd /opt/; mkdir gpybinds; cd gpybinds;\
###    tar xzf /builder/gpstk/gpstk_py_binds.tar.gz;\
###    python setup.py install
###
#### Get pdftk pkgfile from AUR
###RUN mkdir builder/pdftk;\
###    cd builder/pdftk/;\
###    git clone https://aur.archlinux.org/pdftk-bin.git;\
###    git clone https://aur.archlinux.org/libgcj17-bin.git;\
###    chown -R builder:builder /builder;\
###    cd libgcj17-bin;\
###    source ./PKGBUILD;\
###    pacman -S --noconfirm ${depends[@]};\
###    su builder -c "makepkg -s";\
###    pacman -U --noconfirm libgcj17*.pkg.*;\
###    cd ../pdftk-bin;\
###    source ./PKGBUILD;\
###    pacman -S --noconfirm ${depends[@]};\
###    su builder -c "makepkg -s"
###
#############################################
####   End General Build First Stage        #
#############################################
###
#################################
#### gLAB only Builds on UBUNTU #
#################################
###
###FROM ubuntu:latest
###
#### Install Dependencies and updates
###RUN apt update && apt -y --no-install-recommends install build-essential curl
###RUN apt-get install -y --reinstall ca-certificates
###
###COPY gLAB/ gLAB/
###
###RUN cd gLAB/;\
###    ./build.sh
###
###FROM archlinux:latest 
###
###
#### Install gosu
###COPY docker/install_scripts/* ./
###RUN ./install_gosu.sh
###
###ENV PROY_HOME=/proyecto
###
#### WORKAROUND for glibc 2.33 and old Docker
#### See https://github.com/actions/virtual-environments/issues/2658
#### Thanks to https://github.com/lxqt/lxqt-panel/pull/1562
###RUN patched_glibc=glibc-linux4-2.33-4-x86_64.pkg.tar.zst && \
###    curl -LO "https://repo.archlinuxcn.org/x86_64/$patched_glibc" && \
###    bsdtar -C / -xvf "$patched_glibc"
###
#### Install dependencies
###RUN pacman -Syu --noconfirm boost-libs python npm proj poppler;
###
###COPY --from=0 /builder/rtklib/rtklib-git/*.pkg.* .
###COPY --from=0 /builder/gpstk/*.pkg.* .
###
#### Install RtkLib and GpsTK
###RUN pacman -U --noconfirm gpstk*.pkg.* rtklib*.pkg.*;\
###    rm -f rtklib*.pkg.* gpstk*.pkg.*;\
###    pacman -Scc --noconfirm
###
#### Install anubis and gebPP
###COPY --from=0 /anubis/app/anubis /usr/local/bin/anubis
###COPY --from=0 /geb-pp/app/gebPP /usr/local/bin/gebPP
###
###RUN chmod 755 /usr/local/bin/anubis;\
###    chmod 755 /usr/local/bin/gebPP
###
#### Install Glab
###COPY --from=1 /gLAB/bin/* /usr/local/bin/
###
###RUN chmod 755 /usr/local/bin/gLAB_linux;\
###    chmod 755 /usr/local/bin/gLAB_linux_multithread
###
#### Prepare Virtual Environment
###COPY --from=0 /opt/venv /opt/venv
###ENV PATH="/opt/venv/bin:$PATH"
###RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager@2.0;\
###    jupyter labextension install jupyter-matplotlib;\
###    jupyter labextension update --all;\
###    jupyter lab build
###
###RUN mkdir rtklib
###
###COPY /data /rtklib/data
###COPY /confs /rtklib/confs
###
#### Install pyconf, rtklib configuration stripts, as a module on env path
###RUN SPATH=$(python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])') ;\
###    echo $SPATH;\
###    ln -s /rtklib/confs/pyconf "$SPATH/pyconf"
###
#### Install Extra tools
###COPY --from=0 /builder/pdftk/pdftk-bin/*.pkg.* .
###COPY --from=0 /builder/pdftk/libgcj17-bin/*.pkg.* .
###
###RUN pacman -U --noconfirm libgcj17*.pkg.*;\
###    pacman -U --noconfirm pdftk*.pkg.*;\
###    rm -f pdftk*.pkg.* libgcj17*.pkg.*;\
###    pacman -Scc --noconfirm
###
#### Entrypoint Prepares working directory and unprivileged userfor jupyter
###COPY docker/gosu_entry.sh /usr/local/bin/gosu_entry.sh
###RUN chmod +x /usr/local/bin/gosu_entry.sh
###
###COPY notebooks /notebooks
###
###VOLUME /notebooks
###VOLUME /proyecto
###
###ENTRYPOINT ["/usr/local/bin/gosu_entry.sh"]
###
###CMD ["jupyter-lab", "--ip=0.0.0.0", "--port=8889", "--no-browser", "--notebook-dir=/notebooks"]
