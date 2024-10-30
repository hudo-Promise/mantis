# ONE PLATFORM

### Project Deployment
* 项目部署分为正式环境(product) / 开发环境(develop) / 测试环境(testing)
  * 正式环境
    * 开启base_setting 中的 SERVICE_MODE=product 
    * 配置 uwsgi.ini
      * http=0.0.0.0:10001
    * 部署路径 172.16.50.16 /home/OnePlatform
  * 开发环境
    * 开启base_setting 中的 SERVICE_MODE=develop 
    * 配置 uwsgi.ini
      * http=0.0.0.0:10002
    * 部署路径 172.16.50.100 /home/OnePlatform
  * 测试环境
    * 开启base_setting 中的 SERVICE_MODE=testing
    * 配置 uwsgi.ini
      * http=0.0.0.0:10003
    * 部署路径 172.16.50.100 /home/OnePlatform

### Project Beginning
* docker-compose -f docker_file/docker-compose-pro.yml up -d op11-pro
* docker-compose -f docker_file/docker-compose-dev.yml up -d op11-dev
* docker-compose -f docker_file/docker-compose-test.yml up -d op11-test

### Project ending
* docker-compose -f docker_file/docker-compose-pro.yml down op11-pro
* docker-compose -f docker_file/docker-compose-dev.yml down op11-dev
* docker-compose -f docker_file/docker-compose-test.yml down op11-test

### Local Debugging
* 通过 run.py 启动本地调试环境

### Python Dependent Environment
* 详见 requirements.txt

### Mysql Migrate
* 通过auxiliary_tool做数据初始化配置

### Redis
* docker 部署

### Front-end Project Address
* ssh://git@172.16.50.3:2022/leihao/one-platform.git
* http://172.16.50.3/leihao/one-platform.git
