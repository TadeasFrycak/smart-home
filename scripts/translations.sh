echo ""
echo "Looking for strings..."
echo ""

pybabel extract -F ../config/babel.ini -k lazy_gettext -k lazy_ngettext --project="Smart Home" --version="1.16" -o ../base.pot ../
#pybabel extract -F ../config/babel.ini -k lazy_gettext -k lazy_ngettext --omit-header -o ../base.pot ../

echo ""
echo "Adding language files..."
echo ""

pybabel update -i ../base.pot -d ../translations
#pybabel update -i ../base.pot -d ../translations --omit-header

echo ""
read -n 1 -s -r -p "Please translate strings and then press any key to continue"
echo ""
echo ""

pybabel compile -f -d ../translations

echo ""
echo "Done."
echo ""