var script1 = document.createElement('script');
var script2 = document.createElement('script');
var script3 = document.createElement('script');
script1.src = '/js/pdf.js';
document.head.appendChild(script1);
script2.src = '/js/pdf.worker.js';
document.head.appendChild(script2);

//*** Rendering the PDF document ***
function renderPDF(pdfFile) {
  // svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  pdfjsLib.getDocument(pdfFile).then(function(pdf) {
    // Get div#container and cache it for later use
    var container = document.getElementById('container');

    // Loop from 1 to total_number_of_pages in PDF document
    for (var i = 1; i <= pdf.numPages; i++) {
      // Get desired page
      pdf.getPage(i).then(function(page) {
        var scale = 2;
        var viewport = page.getViewport(scale);
        var div = document.createElement('div');

        // Set id attribute with page-#{pdf_page_number} format
        div.setAttribute('id', 'page-' + (page.pageIndex + 1));

        // This will keep positions of child elements as per our needs
        div.setAttribute('style', 'position: relative');
        div.style.width = viewport.width + 'px';

        // Append div within div#container
        container.appendChild(div);

        // Create a new Canvas element
        canvas = document.createElement('canvas');
        canvas.setAttribute('class', 'canvas');

        // Append Canvas within div#page-#{pdf_page_number}
        context = canvas.getContext('2d');
        canvas.height = viewport.height;
        canvas.width = viewport.width;
        // canvas.style.position = 'absolute';
        div.appendChild(canvas);

        var renderContext = {
          canvasContext: context,
          viewport: viewport
        };

        // Render PDF page
        page.render(renderContext);
      });
    }
  });
}
