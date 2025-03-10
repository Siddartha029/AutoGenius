async function compare() {
    const vehicle1 = document.getElementById('vehicle1').value;
    const vehicle2 = document.getElementById('vehicle2').value;

    const response = await fetch(`/compare?vehicle1=${vehicle1}&vehicle2=${vehicle2}`);
    const data = await response.json();

    if (data.specs1 && data.specs2) {
        const comparisonDiv = document.getElementById('comparison');
        comparisonDiv.innerHTML = `<h3>Vehicle Comparison</h3><table id="specs-table"><thead><tr><th>Specification</th><th>${vehicle1}</th><th>${vehicle2}</th></tr></thead><tbody></tbody></table>`; // Updated header
        const tableBody = document.querySelector('#specs-table tbody');

        for (const key in data.specs1) {
            if (data.specs2.hasOwnProperty(key)) {
                const row = tableBody.insertRow();
                const cell1 = row.insertCell(0);
                const cell2 = row.insertCell(1);
                const cell3 = row.insertCell(2);

                cell1.textContent = key.replace(/_/g, " ");
                cell2.textContent = data.specs1[key];
                cell3.textContent = data.specs2[key];
            }
        }
        // Save the comparison
        saveComparison(vehicle1, vehicle2, data);
    }
     else {
        alert(data.error || 'Comparison failed. Please enter the vehicle names exactly as they appear in the dataset.');
    }
}

