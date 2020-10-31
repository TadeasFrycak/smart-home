echo ""
echo "Hledám texty..."
echo ""

pybabel extract -F ../config/babel.ini -k lazy_gettext -k lazy_ngettext --project="Smart Home" --version=1.14 -o ../base.pot ../

echo ""
echo "Doplňuji jazykové soubory..."
echo ""

pybabel update -i ../base.pot -d ../translations

echo ""
read -n 1 -s -r -p "Nyní prosím přepiště jazykové soubory a poté zmáčkněte libovolnou klávesu"
echo ""
echo ""

pybabel compile -f -d ../translations
