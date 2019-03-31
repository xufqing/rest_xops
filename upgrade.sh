echo "Upgrading rest_xops"
echo "----------------"
cd $(dirname $0)
echo -e "\033[33m 获取更新\033[0m"
git pull
cd init_data/
