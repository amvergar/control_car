export async function loadReports() {
    const response = await fetch("http://127.0.0.1:8000/reports");
    const data = await response.json();

    const container = document.getElementById("reports");
    container.innerHTML = `
        <h3>Rendimiento: ${data.rendimiento} km/l</h3>
        <h3>Costo mensual: $${data.costoMensual}</h3>
        <h3>Alertas: ${data.alertas.join(", ")}</h3>
    `;
}

loadReports();
