let refreshActif = true;
let intervalID = null;
const URL_CSV = document.body.dataset.csvUrl;
const URL_JSON = document.body.dataset.jsonUrl;

function getCurrentParams() {
    const form = document.getElementById('filtre-form');
    const formData = new FormData(form);
    return new URLSearchParams(formData).toString();
}

function mettreAJourGraphiques(data) {
    const container = document.getElementById("graph-container");
    if (!container) return;
    container.innerHTML = '';

    const grouped = {};
    data.forEach(d => {
        const key = d.capteur;
        if (!grouped[key]) grouped[key] = [];
        grouped[key].push({
            timestamp: d.timestamp,
            temperature: d.temperature
        });
    });

    Object.entries(grouped).forEach(([nom, points]) => {
        const sorted = points.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
        const derniersPoints = sorted.slice(-100);
        const labels = derniersPoints.map(p => p.timestamp);
        const values = derniersPoints.map(p => p.temperature);

        const title = document.createElement("h3");
        title.textContent = nom;
        container.appendChild(title);

        const canvas = document.createElement("canvas");
        canvas.height = 300;
        container.appendChild(canvas);

        new Chart(canvas, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: `Température (${nom})`,
                    data: values,
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 2
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        type: 'time',
                        time: { 
                            parser: 'yyyy-MM-dd HH:mm:ss',
                            tooltipFormat: 'dd/MM/yyyy HH:mm:ss',
                            unit: 'minute'
                        },
                        title: { display: true, text: 'Temps' }
                    },
                    y: {
                        title: { display: true, text: 'Température (°C)' }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    });
}

function chargerDonnees() {
    const url = URL_JSON + '?' + getCurrentParams();
    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error('Erreur réseau');
            return response.json();
        })
        .then(data => {
            const liste = document.getElementById('liste-donnees');
            liste.innerHTML = '';
            if (data.length === 0) {
                const li = document.createElement('li');
                li.textContent = 'Aucune donnée trouvée.';
                liste.appendChild(li);
            } else {
                data.forEach(d => {
                    const li = document.createElement('li');
                    li.textContent = `${d.timestamp} — ${d.capteur} — ${d.temperature} °C`;
                    liste.appendChild(li);
                });
            }
            mettreAJourGraphiques(data);
        })
        .catch(err => {
            console.error('Erreur AJAX:', err);
        });
}

function lancerAutoRefresh() {
    if (!intervalID) {
        intervalID = setInterval(() => {
            if (refreshActif) chargerDonnees();
        }, 5000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('toggle-refresh');
    const form = document.getElementById('filtre-form');
    const csvBtn = document.getElementById('csv-export');

    csvBtn.href = URL_CSV + '?' + getCurrentParams();

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        chargerDonnees();
        csvBtn.href = URL_CSV + '?' + getCurrentParams();
    });

    btn.addEventListener('click', () => {
        refreshActif = !refreshActif;
        if (refreshActif) {
            btn.textContent = '⏸ Pause auto-refresh';
            btn.classList.add('pause');
            chargerDonnees();
        } else {
            btn.textContent = '▶️ Reprendre auto-refresh';
            btn.classList.remove('pause');
        }
    });

    chargerDonnees();
    lancerAutoRefresh();
});