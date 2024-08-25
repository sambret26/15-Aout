const fix = false;
const categorySexPairs = [
    { category: "J", sex: "M" }, //0
    { category: "J", sex: "F" }, //1
    { category: "S", sex: "M" }, //2
    { category: "S", sex: "F" },  //3
    { category: "35+", sex: "M" }, //4
    { category: "35+", sex: "F" }, //5
    { category: "45+", sex: "M" }, //6
    { category: "45+", sex: "F" }, //7
    { category: "55+", sex: "M" }, //8
    { category: "55+", sex: "F" }, //9
    { category: "65+", sex: "M" } //10
];

let currentPairIndex = 0;
let currentPair = categorySexPairs[currentPairIndex];

async function update() {
  try {
    const dataList = document.getElementById('dataList');
    const dataList2 = document.getElementById('dataList2');
    const header2 = document.getElementById('header2');
    if (!dataList || !dataList2 || !header2) return;

    const response = await fetch("./DB.db");
    const data = await response.arrayBuffer();
    initDatabase(data);
  } catch (error) {
    console.error('Erreur lors du chargement de la base de données :', error);
  }
}

async function initDatabase(data) {
  try {
    const SQL = await initSqlJs({ locateFile: filename => './sql-wasm.wasm' });
    const db = new SQL.Database(new Uint8Array(data));
    const query = "SELECT * FROM Runners ORDER BY Ranking";
    const query2 = `SELECT * FROM Runners WHERE Category = '${currentPair.category}' AND Sex = '${currentPair.sex}' ORDER BY Ranking`;
    const [result, result2] = [db.exec(query), db.exec(query2)];
    const values = result[0]?.values || [];
    const values2 = result2[0]?.values || [];

    updateDataList(document.getElementById('dataList'), "toutes", values);
    applyAnimation(document.getElementById('dataList'), values.length);
    createDynamicStyle(values.length);

    if (values.length !== 0 && values2.length === 0) {
        naviguerPaires();
        return; // Reviens immédiatement pour éviter de mettre à jour avec des données vides
    }

    updateDataList(document.getElementById('dataList2'), currentPair.category, values2);
    updateHeader(document.getElementById('header2'));
  } catch (error) {
    console.error('Erreur lors de l\'initialisation de la base de données SQLite :', error);
  }
}

function updateDataList(dataList, category, values) {
  if (!dataList) return;

  const html = values.map(row => `
    <li>
      <div>${category === "toutes" ? row[4] : row[6]}</div>
      <div>${row[1]} ${row[2]}</div>
      <div class="toalign">${row[3]}</div>
      <div class="toalign">${row[5]}</div>
      <div class="toalign">${category === "toutes" ? row[6] : row[4]}</div>
      <div class="toalign">${row[7]}</div>
      <div class="toalign">${row[8]}</div>
      <div class="toalign">${row[9]}</div>
    </li>
  `).join('');
  dataList.innerHTML = html;
}

function updateHeader(header) {
  if (!header) return;
  
  header.innerHTML = "";
  const text = document.createElement("h2");
  text.textContent = `Classement de la catégorie ${getCategoryLabel(currentPair.category)} ${getSexLabel(currentPair.sex)}`;
  header.appendChild(text);
}

function applyAnimation(dataList, length) {
  if (!dataList) return;
  const duration = length * 0.5; // Même durée que dans createDynamicStyle
  dataList.style.animation = length > 22 ? `scrollPauseAnimation ${duration}s linear infinite` : null;
}


function createDynamicStyle(length) {
  let dynamicStyle = document.getElementById('dynamic-style');
  if (!dynamicStyle) {
      dynamicStyle = document.createElement('style');
      dynamicStyle.id = 'dynamic-style';
      document.head.appendChild(dynamicStyle);
  }

  const scrollSpeed = 10; // Le temps en secondes pour que l'élément défile de haut en bas
  const scrollDuration = scrollSpeed * (length -22); // Durée totale pour le défilement
  const pauseDuration = 75; // Durée de la pause en secondes
  const totalDuration = pauseDuration*2 + scrollDuration;
  const pausePourcentage = ((pauseDuration / totalDuration) * 100).toFixed(2)
  dynamicStyle.textContent = `
      @keyframes scrollPauseAnimation {
          0% {
              transform: translateY(0);
          }
          ${pausePourcentage}% {
              transform: translateY(0);
          }
          ${100 - pausePourcentage}% {
              transform: translateY(calc(-100% + 85vh));
          }
          100% {
              transform: translateY(calc(-100% + 85vh));
          }
      }
  `;
}

function setHeader(container, category) {
  if (!container) return;

  const columns = category === "toutes"
    ? ["Class.", "Nom", "Sexe", "Cat.", "Class. Cat.", "Class. Sexe", "Dossard", "Temps"]
    : ["Class. Cat.", "Nom", "Sexe", "Cat.", "Class. Géné.", "Class. Sexe", "Dossard", "Temps"];

  const headerHTML = `<li class="header">${columns.map(col => `<div>${col}</div>`).join('')}</li>`;
  container.innerHTML = headerHTML;
}

function naviguerPaires() {
  if (fix) return;
  currentPairIndex = (currentPairIndex + 1) % categorySexPairs.length;
  currentPair = categorySexPairs[currentPairIndex];
  update()
}

function getSexLabel(sex) {
  const sexLabels = { "F": "Femmes", "M": "Hommes" };
  return sexLabels[sex] || sex;
}

function getCategoryLabel(category) {
  const categoryLabels = { "J": "Jeunes", "S": "Séniors" };
  return categoryLabels[category] || category;
}

document.addEventListener('DOMContentLoaded', () => {
  console.log("Starting");
  const dataListHeader = document.getElementById('dataListHeader');
  const dataListHeader2 = document.getElementById('dataListHeader2');
  
  setHeader(dataListHeader, "toutes");
  setHeader(dataListHeader2, currentPair.category);

  setInterval(naviguerPaires, 10000);

  update();
});