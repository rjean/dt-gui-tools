# parameters
ARG REPO_NAME="dt-gui-tools"
ARG DESCRIPTION="Provides access to GUI-based ROS tools (e.g., rviz, rqt_image_view)"
ARG MAINTAINER="Andrea F. Daniele (afdaniele@ttic.edu)"
# pick an icon from: https://fontawesome.com/v4.7.0/icons/
ARG ICON="desktop"

# novnc and websockify versions to use
ARG NOVNC_VERSION="35dd3c2"
ARG WEBSOCKIFY_VERSION="3646575"

# ==================================================>
# ==> Do not change the code below this line
ARG ARCH=arm32v7
ARG DISTRO=daffy
ARG BASE_TAG=${DISTRO}-${ARCH}
ARG BASE_IMAGE=dt-core
ARG LAUNCHER=default

# define base image
FROM duckietown/${BASE_IMAGE}:${BASE_TAG} as base

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

# install python3 dependencies
COPY ./dependencies-py3.txt "${REPO_PATH}/"
RUN pip3 install -r ${REPO_PATH}/dependencies-py3.txt

# copy the source code
COPY ./packages "${REPO_PATH}/packages"

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

## nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

# install ffmpeg
COPY assets/vnc/install-ffmpeg /tmp/
RUN /tmp/install-ffmpeg ${ARCH}

# install backend dependencies
COPY assets/vnc/install-backend-deps /tmp/
COPY assets/vnc/image/usr/local/lib/web/backend/requirements.txt /tmp/
RUN /tmp/install-backend-deps

# copy novnc stuff to the root of the container
COPY assets/vnc/image /


#### => Substep: Frontend builder
##
##  NOTE:   This substep always runs in an amd64 image regardless of the architecture of
##          final image. As a result, this Dockerfile can be run only on amd64 machines
##          with QEMU enabled.
##
##
FROM ubuntu:xenial as builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        git

# nodejs
RUN curl -sL https://deb.nodesource.com/setup_9.x | bash - \
    && apt-get install -y \
        nodejs

# yarn
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
    && apt-get update \
    && apt-get install -y yarn

# fetch noVNC
ARG NOVNC_VERSION
RUN git clone https://github.com/novnc/noVNC /src/web/static/novnc \
    && git -C /src/web/static/novnc checkout ${NOVNC_VERSION}

# fetch websockify
ARG WEBSOCKIFY_VERSION
RUN git clone https://github.com/novnc/websockify /src/web/static/websockify \
    && git -C /src/web/static/websockify checkout ${WEBSOCKIFY_VERSION}

# build frontend
COPY assets/vnc/web /src/web
RUN cd /src/web \
    && yarn \
    && npm run build
##
##
#### <= Substep: Frontend builder


# jump back to the base image and copy frontend from builder stage
FROM base
COPY --from=builder /src/web/dist/ /usr/local/lib/web/frontend/

# configure novnc
ENV HTTP_PORT 8087
