if (window.location.href === "https://webdt.edunet.net/pdf") {
    console.log("extracting...");
} else if (window.location.href === "https://webdt.edunet.net/viewer/") {
    console.log("viewer not supported");
} else {
    console.log("invalid url.");
}

var scriptText = document.querySelectorAll('body > script:nth-child(35)')[0].textContent;

var match = scriptText.match(/if \("pdf" == "pdf"\) {\s+parent\.contentInformationURL = "(.*?)";/);
if (match) {
    var pdfLink = match[1];
    console.log("extracted pdf link:", pdfLink);

    fetch(pdfLink, { headers: { 'Referer': 'https://webdt.edunet.net/' } })
        .then(response => response.blob())
        .then(blob => {
            var link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = document.querySelector('#toc_bookNm').textContent + ".pdf";
            link.click();
        })
        .catch(error => console.error("error:", error));
} else {
    console.log("failed to extract pdf link");
}
