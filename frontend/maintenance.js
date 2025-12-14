export async function loadMaintenance() {
    const response = await fetch("http://127.0.0.1:8000/maintenance");
    const records = await response.json();

    const container = document.getElementById("maintenance");
    container.innerHTML = records.map(r => `
        <div>
            ${r.fecha} - ${r.descripcion} - $${r.costo}
        </div>
    `).join("");
}

loadMaintenance();
