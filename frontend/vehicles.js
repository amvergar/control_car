export async function loadVehicles() {
    const response = await fetch("http://127.0.0.1:8000/vehicles");
    const vehicles = await response.json();

    const container = document.getElementById("vehicles");
    container.innerHTML = vehicles.map(v => `
        <div>
            <strong>${v.placa}</strong> - ${v.modelo} (${v.anio})
        </div>
    `).join("");
}
loadVehicles();

