#!/bin/bash
cd ~/WeChatTicket #此处替换成你在服务器上的代码部署目录
git pull origin master #在服务器上拉取分支
echo 'travis build done!'
