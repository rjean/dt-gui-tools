# parameters
ARG REPO_NAME="dt-gui-tools"
ARG DESCRIPTION="Provides access to GUI-based ROS tools (e.g., rviz, rqt_image_view)"
ARG MAINTAINER="Andrea F. Daniele (afdaniele@ttic.edu)"
# pick an icon from: https://fontawesome.com/v4.7.0/icons/
ARG ICON="desktop"

# ==================================================>
# ==> Do not change the code below this line
ARG ARCH=arm32v7
ARG DISTRO=daffy
ARG BASE_TAG=${DISTRO}-${ARCH}
ARG BASE_IMAGE=dt-ros-commons
ARG LAUNCHER=default

# define base image
FROM duckietown/${BASE_IMAGE}:${BASE_TAG}

# recall all arguments
ARG ARCH
ARG DISTRO
ARG REPO_NAME
ARG DESCRIPTION
ARG MAINTAINER
ARG ICON
ARG BASE_TAG
ARG BASE_IMAGE
ARG LAUNCHER

# check build arguments
RUN dt-build-env-check "${REPO_NAME}" "${MAINTAINER}" "${DESCRIPTION}"

# define/create repository path
ARG REPO_PATH="${CATKIN_WS_DIR}/src/${REPO_NAME}"
ARG LAUNCH_PATH="${LAUNCH_DIR}/${REPO_NAME}"
RUN mkdir -p "${REPO_PATH}"
RUN mkdir -p "${LAUNCH_PATH}"
WORKDIR "${REPO_PATH}"

# keep some arguments as environment variables
ENV DT_MODULE_TYPE "${REPO_NAME}"
ENV DT_MODULE_DESCRIPTION "${DESCRIPTION}"
ENV DT_MODULE_ICON "${ICON}"
ENV DT_MAINTAINER "${MAINTAINER}"
ENV DT_REPO_PATH "${REPO_PATH}"
ENV DT_LAUNCH_PATH "${LAUNCH_PATH}"
ENV DT_LAUNCHER "${LAUNCHER}"

# install apt dependencies
COPY ./dependencies-apt.txt "${REPO_PATH}/"
RUN dt-apt-install ${REPO_PATH}/dependencies-apt.txt

# install python dependencies
COPY ./dependencies-py.txt "${REPO_PATH}/"
RUN pip install -r ${REPO_PATH}/dependencies-py.txt

# install python3 dependencies
COPY ./dependencies-py3.txt "${REPO_PATH}/"
RUN pip3 install -r ${REPO_PATH}/dependencies-py3.txt

# copy the source code
COPY . "${REPO_PATH}/"

# build packages
RUN . /opt/ros/${ROS_DISTRO}/setup.sh && \
  catkin build \
    --workspace ${CATKIN_WS_DIR}/

# install launcher scripts
COPY ./launchers/. "${LAUNCH_PATH}/"
COPY ./launchers/default.sh "${LAUNCH_PATH}/"
RUN dt-install-launchers "${LAUNCH_PATH}"

# define default command
CMD ["bash", "-c", "dt-launcher-${DT_LAUNCHER}"]

# store module metadata
LABEL org.duckietown.label.module.type="${REPO_NAME}" \
    org.duckietown.label.module.description="${DESCRIPTION}" \
    org.duckietown.label.module.icon="${ICON}" \
    org.duckietown.label.architecture="${ARCH}" \
    org.duckietown.label.code.location="${REPO_PATH}" \
    org.duckietown.label.code.version.distro="${DISTRO}" \
    org.duckietown.label.base.image="${BASE_IMAGE}" \
    org.duckietown.label.base.tag="${BASE_TAG}" \
    org.duckietown.label.maintainer="${MAINTAINER}"
# <== Do not change the code above this line
# <==================================================

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

# configure HOME environment (do not change)
ENV USER=duckie
ENV PASSWD=quackquack
ENV UID=1000
ENV GID=1000
ENV HOME=/home/$USER
RUN mkdir -p ${HOME}

# configure NOVNC (do not change)
ENV NO_VNC_HOME=$HOME/noVNC
ENV NO_VNC_PORT=6901
RUN mkdir -p ${NO_VNC_HOME}

# configure VNC (do not change)
ENV DISPLAY=:1
ENV VNC_PORT=5901
ENV VNC_VIEW_ONLY=false
ENV VNC_PW=$PASSWD

# generate locale
ENV LANG='en_US.UTF-8'
ENV LANGUAGE='en_US:en'
ENV LC_ALL='en_US.UTF-8'
RUN locale-gen en_US.UTF-8

# install XFCE4
RUN apt-get update \
    && apt-get install -y \
        supervisor \
        xfce4 \
        xfce4-terminal \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y \
        pm-utils \
        xscreensaver*

# create a HOME for novnc
ADD ./assets/home/. $HOME/

# install xvnc-server and noVNC (HTML5-based VNC viewer)
RUN ${REPO_PATH}/assets/install/tigervnc.sh
RUN ${REPO_PATH}/assets/install/no_vnc.sh

# configure VNC (customizable section)
ENV VNC_COL_DEPTH=24
ENV VNC_RESOLUTION=1920x1080

# expose ports
EXPOSE $VNC_PORT $NO_VNC_PORT
