#!/var/lib/geonode/bin/python
import sys, os
import boto

from django.conf import settings

log = open("/var/log/tomcat7/post_commit_hook.out","w")
log.write("Log 2 opened")

if len(sys.argv) == 2:
    msg_geogit = sys.argv[1]
    sns = boto.connect_sns(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    topic = settings.AWS_SNS_TOPIC
    if (not (topic is None)) and (len(topic)>0):
        msg_sns = "User ___ just commited an update to the ____ GeoGit Repo on the ____ GeoNode at ______.\n\nThe commit message was:\n\n"+msg_geogit+"\n\nThis message was automatically generated.  Please contact the system administrator of the specified GeoNode to adjust your preferences."

        res = sns.publish(topic, msg_sns)
    else:
        log.write( "Topic was invalid")
else:
    log.write("Invalid program call")

log.close()
