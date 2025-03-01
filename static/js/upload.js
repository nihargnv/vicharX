document.addEventListener("DOMContentLoaded", () => {
  // File upload handling
  const dropArea = document.getElementById("drop-area")
  const fileInput = document.getElementById("file-input")
  const uploadQueue = document.getElementById("upload-queue")

  if (dropArea && fileInput) {
    // Prevent default drag behaviors
    ;["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
      dropArea.addEventListener(eventName, preventDefaults, false)
    })

    function preventDefaults(e) {
      e.preventDefault()
      e.stopPropagation()
    }
    // Highlight drop area when item is dragged over it
    ;["dragenter", "dragover"].forEach((eventName) => {
      dropArea.addEventListener(eventName, highlight, false)
    })
    ;["dragleave", "drop"].forEach((eventName) => {
      dropArea.addEventListener(eventName, unhighlight, false)
    })

    function highlight() {
      dropArea.classList.add("dragover")
    }

    function unhighlight() {
      dropArea.classList.remove("dragover")
    }

    // Handle dropped files
    dropArea.addEventListener("drop", handleDrop, false)

    function handleDrop(e) {
      const dt = e.dataTransfer
      const files = dt.files

      handleFiles(files)
    }

    // Handle selected files
    fileInput.addEventListener("change", function () {
      handleFiles(this.files)
    })

    // Click on drop area to trigger file input
    dropArea.addEventListener("click", () => {
      fileInput.click()
    })

    function handleFiles(files) {
      if (!files.length) return

      // Convert FileList to Array
      const filesArray = Array.from(files)

      // Process each file
      filesArray.forEach((file) => {
        uploadFile(file)
      })
    }

    function uploadFile(file) {
      // Create upload item
      const uploadItem = document.createElement("li")
      uploadItem.className = "upload-item"

      // Determine icon based on file type
      let iconClass = "fa-file"
      if (file.type.includes("image")) {
        iconClass = "fa-file-image"
      } else if (file.type.includes("pdf")) {
        iconClass = "fa-file-pdf"
      } else if (file.type.includes("word")) {
        iconClass = "fa-file-word"
      } else if (file.type.includes("excel") || file.type.includes("spreadsheet")) {
        iconClass = "fa-file-excel"
      }

      // Format file size
      const fileSize = formatFileSize(file.size)

      uploadItem.innerHTML = `
                <div class="upload-item-icon">
                    <i class="fas ${iconClass}"></i>
                </div>
                <div class="upload-item-info">
                    <div class="upload-item-name">${file.name}</div>
                    <div class="upload-item-size">${fileSize}</div>
                    <div class="upload-progress">
                        <div class="upload-progress-bar" style="width: 0%"></div>
                    </div>
                </div>
                <div class="upload-item-status">
                    <span>0%</span>
                </div>
            `

      // Add to upload queue
      if (uploadQueue) {
        uploadQueue.appendChild(uploadItem)
      }

      // Simulate upload progress
      simulateUpload(uploadItem, file)
    }

    function simulateUpload(uploadItem, file) {
      const progressBar = uploadItem.querySelector(".upload-progress-bar")
      const statusText = uploadItem.querySelector(".upload-item-status span")

      let progress = 0
      const interval = setInterval(() => {
        progress += Math.random() * 10
        if (progress > 100) progress = 100

        progressBar.style.width = `${progress}%`
        statusText.textContent = `${Math.round(progress)}%`

        if (progress === 100) {
          clearInterval(interval)

          // Simulate processing delay
          setTimeout(() => {
            statusText.innerHTML = '<i class="fas fa-check" style="color: var(--success-color);"></i>'

            // Add to documents (in a real app, this would come from the server)
            addUploadedDocument(file)
          }, 1000)
        }
      }, 300)
    }

    function formatFileSize(bytes) {
      if (bytes === 0) return "0 Bytes"

      const k = 1024
      const sizes = ["Bytes", "KB", "MB", "GB"]
      const i = Math.floor(Math.log(bytes) / Math.log(k))

      return Number.parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i]
    }

    function addUploadedDocument(file) {
      // In a real app, this would get data from the server after processing
      // For demo, we'll create a mock document

      // Generate random category
      const categories = ["invoice", "contract", "resume", "report"]
      const randomCategory = categories[Math.floor(Math.random() * categories.length)]

      // Generate random tags based on category
      let tags = []
      if (randomCategory === "invoice") {
        tags = ["finance", "2025", Math.random() > 0.5 ? "paid" : "pending"]
      } else if (randomCategory === "contract") {
        tags = ["legal", Math.random() > 0.5 ? "employment" : "service", "signed"]
      } else if (randomCategory === "resume") {
        tags = ["hiring", Math.random() > 0.5 ? "developer" : "designer", "candidate"]
      } else {
        tags = ["report", Math.random() > 0.5 ? "quarterly" : "annual", "2025"]
      }

      // Create new document
      const newDoc = {
        id: Date.now(),
        name: file.name,
        category: randomCategory,
        tags: tags,
        preview: "/placeholder.svg?height=150&width=120",
        uploadDate: new Date().toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" }),
        fileSize: formatFileSize(file.size),
        extractedText: `This is extracted text from ${file.name}.\nCategory: ${randomCategory}\nUploaded: ${new Date().toLocaleDateString()}`,
      }

      // Add to documents container
      const documentsContainer = document.querySelector(".documents-container")
      if (documentsContainer) {
        const docTile = document.createElement("div")
        docTile.className = "document-tile"
        docTile.setAttribute("data-id", newDoc.id)

        docTile.innerHTML = `
                    <div class="document-preview">
                        <img src="${newDoc.preview}" alt="${newDoc.name}">
                    </div>
                    <div class="document-info">
                        <h3 class="document-name">${newDoc.name}</h3>
                        <span class="document-category ${newDoc.category}">${newDoc.category}</span>
                        <div class="document-tags">
                            ${newDoc.tags.map((tag) => `<span class="tag">${tag}</span>`).join("")}
                        </div>
                    </div>
                `

        documentsContainer.prepend(docTile)

        // Update document click handlers
        initDocumentClickHandlers()

        // Update analytics
        updateAnalytics()
      }
    }
  }
})

// This function is defined in dashboard.js but we need it here too
function initDocumentClickHandlers() {
  const documentTiles = document.querySelectorAll(".document-tile")
  const metadataPanel = document.getElementById("metadata-panel")

  documentTiles.forEach((tile) => {
    tile.addEventListener("click", function () {
      const docId = this.getAttribute("data-id")

      // In a real app, we would fetch document data from the server
      // For demo, we'll use the DOM to get the data
      const name = this.querySelector(".document-name").textContent
      const category = this.querySelector(".document-category").textContent
      const preview = this.querySelector(".document-preview img").src

      // Get tags
      const tags = []
      this.querySelectorAll(".tag").forEach((tag) => {
        tags.push(tag.textContent)
      })

      // Update metadata panel
      document.getElementById("document-name").textContent = name
      document.getElementById("document-category").innerHTML = `Category: <span>${category}</span>`
      document.getElementById("upload-date").textContent = new Date().toLocaleDateString("en-US", {
        month: "long",
        day: "numeric",
        year: "numeric",
      })
      document.getElementById("file-size").textContent = "1.2 MB" // Mock size

      // Update tags
      const tagsContainer = document.getElementById("ai-tags")
      tagsContainer.innerHTML = ""
      tags.forEach((tag) => {
        const tagElement = document.createElement("span")
        tagElement.className = "tag"
        tagElement.textContent = tag
        tagsContainer.appendChild(tagElement)
      })

      // Update extracted text
      document.getElementById("extracted-text").innerHTML =
        `<p>This is extracted text from ${name}.\nCategory: ${category}\nUploaded: ${new Date().toLocaleDateString()}</p>`

      // Update preview
      document.getElementById("document-preview").src = preview

      // Open metadata panel
      metadataPanel.classList.add("open")
    })
  })
}

// Update analytics after new document is added
function updateAnalytics() {
  // Count documents by category
  const documents = document.querySelectorAll(".document-tile")
  const categories = {}

  documents.forEach((doc) => {
    const category = doc.querySelector(".document-category").textContent
    if (categories[category]) {
      categories[category]++
    } else {
      categories[category] = 1
    }
  })

  // Update total documents count
  const totalDocumentsElement = document.getElementById("total-documents")
  if (totalDocumentsElement) {
    totalDocumentsElement.textContent = documents.length
  }

  // Update categories count
  const totalCategoriesElement = document.getElementById("total-categories")
  if (totalCategoriesElement) {
    totalCategoriesElement.textContent = Object.keys(categories).length
  }

  // Update chart
  //The updateDocumentChart variable is undeclared.  Assuming it's a function defined elsewhere.  This is a placeholder.  Replace with actual implementation.
  function updateDocumentChart(categories) {
    //Implementation to update chart goes here.  This is a placeholder.
    console.log("Chart updated with categories:", categories)
  }
  updateDocumentChart(categories)
}

