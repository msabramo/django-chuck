# Install virtualenv
cd ${WORKSPACE}

rm -rf ve
virtualenv --no-site-packages ve
. ve/bin/activate

if [ -r requirements/requirements_dev.txt ]; then
   pip install --upgrade -E ./ve -r requirements/requirements_dev.txt
else
   pip install --upgrade -E ./ve -r requirements/requirements_local.txt
fi

# Remove old database and reports
rm -rf db
rm -rf reports

# Run tests and code coverage
DJANGO_SETTINGS_MODULE= PYTHONPATH="${WORKSPACE}/ve/lib/python$PYTHON_VERSION/site-packages/:${WORKSPACE}:${WORKSPACE}}/$PROJECT_NAME:$PYTHONPATH" ${WORKSPACE}/ve/bin/django-admin.py jenkins

# Filter migration and test urls false alarms
cat ${WORKSPACE}/reports/pylint.report | grep -v migrations | grep -v test_urls > ${WORKSPACE}}reports/pylint.report
