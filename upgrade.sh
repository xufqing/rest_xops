echo "Upgrading rest_xops"
echo "----------------"
cd $(dirname $0)
echo -e "\033[33m 获取更新\033[0m"
git pull
echo -e "\033[33m app更新\033[0m"
dir=$(ls -l apps/ |awk '/^d/ {print $NF}')
for i in $dir
  do
    python manage.py makemigrations $i
  done
python manage.py migrate
echo -e "\033[33m 表结构更新\033[0m"
python manage.py makemigrations rbac
python manage.py makemigrations cmdb
python manage.py makemigrations deployment
python manage.py migrate
echo -e "\033[33m 导入初始数据\033[0m"
python manage.py loaddata init_data/*.json
echo -e "\033[33m 更新完毕,请修改admin密码\033[0m"
