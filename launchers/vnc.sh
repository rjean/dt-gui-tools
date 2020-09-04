#!/bin/bash

source /environment.sh

# initialize launch file
dt-launchfile-init

# YOUR CODE BELOW THIS LINE
# ----------------------------------------------------------------------------


# NOTE: Use the variable DT_REPO_PATH to know the absolute path to your code
# NOTE: Use `dt-exec COMMAND` to run the main process (blocking process)

HOSTNAME=$(hostname)

SOUT=">/dev/null"
if [ "${DEBUG}" = "1" ] || [ "${DEBUG}" = "yes" ] || [ "${DEBUG}" = "true" ]; then
    SOUT=""
fi

# launching app
source /setup-vnc.sh
dt-exec supervisord -n --configuration=/etc/supervisor/supervisord.conf ${SOUT}

sleep 2
echo -e "\n
NoVNC is running.\n
\tOpen the URL http://${HOSTNAME}.local:${HTTP_PORT} in your browser.\n"


# ----------------------------------------------------------------------------
# YOUR CODE ABOVE THIS LINE

# wait for app to end
dt-launchfile-join
