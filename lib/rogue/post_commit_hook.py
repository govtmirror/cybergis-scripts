#!/var/lib/geonode/bin/python

import boto

from django.conf import settings

if len(sys.argv) == 2:
    msg_geogit = sys.argv[1]
    sns = boto.connect_sns(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    topic = settings.AWS_SNS_TOPIC
    if (not (topic is non)) and (len(topic)>0):
        msg_sns = "User ___ just commited an update to the ____ GeoGit Repo on the ____ GeoNode at ______.\n\nThe commit message was:\n\n"+msg_geogit+"\n\nThis message was automatically generated.  Please contact the system administrator of the specified GeoNode to adjust your preferences."

        sns = boto.connect_sns(aws_access_key_id=id,aws_secret_access_key=key)
        res = sns.publish(topic, msg_sns)
    else:
        print "Topic was invalid"
else:
    print "Invalid program call"
