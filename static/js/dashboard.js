async function loadDocuments() {
  const documentsContainer = document.querySelector(".documents-container");
  if (!documentsContainer) return;

  try {
    const response = await fetch("/api/documents/"); // Replace with your actual API endpoint
    if (!response.ok) throw new Error("Failed to fetch documents");

    const documents = await response.json(); // Ensure the response is JSON
    if (!documents || !Array.isArray(documents)) throw new Error("Invalid documents data");

    // Clear container
    documentsContainer.innerHTML = "";

    // Create document tiles
    documents.forEach((doc) => {
      const docTile = document.createElement("div");
      docTile.className = "document-tile";
      docTile.setAttribute("data-id", doc.id);

      docTile.innerHTML = `
        <div class="document-preview">
          <img src="${doc.preview || '/placeholder.svg'}" alt="${doc.name}">
        </div>
        <div class="document-info">
          <h3 class="document-name">${doc.name}</h3>
          <span class="document-category ${doc.category}">${doc.category}</span>
          <div class="document-tags">
            ${doc.tags ? doc.tags.map(tag => `<span class="tag">${tag}</span>`).join("") : ""}
          </div>
        </div>
      `;

      documentsContainer.appendChild(docTile);
    });

    // Update document count
    document.getElementById("total-documents").textContent = documents.length;

    // Update categories count
    const categories = [...new Set(documents.map(doc => doc.category))];
    document.getElementById("total-categories").textContent = categories.length;

    // Update storage used
    const totalSize = documents.reduce((total, doc) => {
      const size = parseFloat(doc.file_size); // Ensure file_size is correctly formatted in backend
      return total + (isNaN(size) ? 0 : size);
    }, 0);

    document.getElementById("storage-used").textContent = totalSize.toFixed(1) + " MB";

    initDocumentClickHandlers();
  } catch (error) {
    console.error("Error loading documents:", error);
  }
}
