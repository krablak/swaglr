echo Moving old data to temp file
rm -rf ./ds-download/tmp/*
mv ./ds-download/* ./ds-download/tmp/
echo Starting data download...
/usr/local/bin/appcfg.py download_data --config_file=bulkloader.yaml --filename=./ds-download/swagclip_export_clip.csv --kind=* --url=http://swagclip.appspot.com/_ah/remote_api
#/usr/local/bin/appcfg.py download_data --config_file=bulkloader.yaml --filename=./ds-download/swagclip_export_user.csv --kind=UserInfo --url=http://swagclip.appspot.com/_ah/remote_api
#/usr/local/bin/appcfg.py download_data --config_file=bulkloader.yaml --filename=./ds-download/swagclip_export_image.csv --kind=Image --url=http://swagclip.appspot.com/_ah/remote_api
