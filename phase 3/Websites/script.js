// JavaScript code to process CSV data and update the website
Papa.parse('parkingdata.csv', {
    download: true,
    header: true,
    skipEmptyLines: true,
    dynamicTyping: true,
    complete: function(results) {
        const data = results.data;

        // Initialize counts
        let vacantCount = 0;
        let occupiedCount = 0;

        // Process the data and calculate counts
        data.forEach((entry) => {
            const status = entry['status'];

            if (status === 'vacant') {
                vacantCount++;
            } else if (status === 'occupied') {
                occupiedCount++;
            }
        });

        // Update the HTML with the counts
        document.getElementById('vacantCount').textContent = vacantCount;
        document.getElementById('occupiedCount').textContent = occupiedCount;
    }
});
