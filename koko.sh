#!/usr/bin/env bash

set -e

BASE_URL="https://raw.githubusercontent.com/Piyush-linux/ds/master"
echo $BASE_URL
TOPICS=(
    "2 CSV HOURUS/AUDIO2HORUS.py"
    "2 CSV HOURUS/CSV2HORUS.py"
    "2 CSV HOURUS/DATABASE2HORUS.py"
    "2 CSV HOURUS/HORUSFrame2HORUS.py"
    "2 CSV HOURUS/JPEG2HORUS.py"
    "2 CSV HOURUS/JSON2HORUS.py"
    "2 CSV HOURUS/MOVIE2HORUSFrame.py"
    "2 CSV HOURUS/XML2HORUS.py"
    "3 fIXERS UTILITIES/DATABINNING.py"
    "3 fIXERS UTILITIES/DU-Outliers.py"
    "3 fIXERS UTILITIES/Fixersutilities.py"
    "3 fIXERS UTILITIES/MeanAverage.py"
    "3 fIXERS UTILITIES/Yoke_Logging.py"
    "4 Retrive/Loading-IP_DATA_ALL.py"
    "4 Retrive/R studio.txt"
    "4 Retrive/Retrieve-Container-Plan.py"
    # 5
    "5 ASSESS/Assess-Best-Fit-Logistics.py"
    "5 ASSESS/Assess-Billboard_2_Visitor.py"
    "5 ASSESS/Assess-Calendar.py"
    "5 ASSESS/Assess-DAG-GPS-unsmoothed.py"
    "5 ASSESS/Assess-DAG-GPS.py"
    "5 ASSESS/Assess-DAG-Location.py"
    "5 ASSESS/Assess-DE-Billboard.py"
    "5 ASSESS/Assess-Financials.py"
    "5 ASSESS/Assess-Forex.py"
    "5 ASSESS/Assess-Warehouse-Address.py"
    "5 ASSESS/Assess-Warehouse-Global.py"
    # 6
    "6 TIME HUB,LINKS/Process-PeopleGoldenNominal.py"
    "6 TIME HUB,LINKS/Process-Sharesforecasting-Data.py"
    "6 TIME HUB,LINKS/Process-Vehicle-Logistics.py"
    "6 TIME HUB,LINKS/Process_LocationHuman enironmentinteraction.py"
    "6 TIME HUB,LINKS/Process_Time.py"
    # 7
    "7 TRANSFORMING DATA/Simple_Linear_Regression.py"
    "7 TRANSFORMING DATA/Transform-Datawarehouse.py"
    "7 TRANSFORMING DATA/Transform-Gunnarsson-Sun-Model.py"
    "7 TRANSFORMING DATA/Transformsuperstep.py"
    # 8
    "8 ORGANIZING DATA/Organise-Forex.py"
    "8 ORGANIZING DATA/Organise-Network-Routing-Company.py"
    "8 ORGANIZING DATA/Organise-Routes.py"
    "8 ORGANIZING DATA/Organise-billboards.py"
    "8 ORGANIZING DATA/Organize-Association-Rule.py"
    "8 ORGANIZING DATA/Organize-Horizontal.py"
    "8 ORGANIZING DATA/Organize-Island.py"
    "8 ORGANIZING DATA/Organize-Secure-Vault.py"
    "8 ORGANIZING DATA/Organize-Vertical.py"
    # 9
    "9 GENERETING DATA/Raport-Network-Routing-Customer.py"
    "9 GENERETING DATA/Report_Billboard.py"
    "9 GENERETING DATA/Report_Reading_Container.py"

)

echo "📦 Available topics:"
echo "---------------------"

for i in "${!TOPICS[@]}"; do
  printf "%d) %s\n" "$((i+1))" "${TOPICS[$i]}"
done

echo
read -p "Select a topic (number): " choice

INDEX=$((choice-1))

if [[ -z "${TOPICS[$INDEX]}" ]]; then
  echo "❌ Invalid selection"
  exit 1
fi

FILE="${TOPICS[$INDEX]}"
urlencode() {
  python3 - <<'EOF' "$1"
import urllib.parse, sys
print(urllib.parse.quote(sys.argv[1]))
EOF
}
ENCODED_FILE=$(urlencode "$FILE")
URL="$BASE_URL/$ENCODED_FILE"

#URL="$BASE_URL/$FILE"
echo $URL
echo "⬇️  Downloading: $FILE"
curl -fsSL "$URL"
curl -fsSL "$URL" -o "file.py"

# chmod +x "$FILE"

# echo "✅ Done"
# echo "👉 Run with: ./$FILE"
