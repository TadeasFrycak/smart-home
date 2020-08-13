echo ""
echo "Hledám texty..."
echo ""

pybabel extract -F babel.cfg -k lazy_gettext --project="Smart Home" --version=1.13 -o messages.pot .

echo ""
echo "Doplňuji jazykové soubory..."
echo ""

pybabel update -i messages.pot -d translations

echo ""
read -n 1 -s -r -p "Nyní prosím přepiště jazykové soubory a poté zmáčkněte libovolnou klávesu"
echo ""
echo ""

pybabel compile -f -d translations
