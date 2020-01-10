docker run -it \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --runtime=nvidia \
    --net=ros \
    -e ROS_MASTER_URI=http://proscore:11311 \
    duckietown/dt-gui-tools:v1-amd64 \
      bash
