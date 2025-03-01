document.addEventListener("DOMContentLoaded", () => {
  // Login form handling
  const loginForm = document.getElementById("login-form")
  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault()

      const email = document.getElementById("email").value
      const password = document.getElementById("password").value

      // Simple validation
      if (!email || !password) {
        alert("Please enter both email and password")
        return
      }

      // Mock authentication - in a real app, this would call the Django backend
      mockAuthentication(email, password)
    })
  }

  // Signup form handling
  const signupForm = document.getElementById("signup-form")
  if (signupForm) {
    signupForm.addEventListener("submit", (e) => {
      e.preventDefault()

      const fullname = document.getElementById("fullname").value
      const email = document.getElementById("email").value
      const password = document.getElementById("password").value
      const confirmPassword = document.getElementById("confirm-password").value

      // Simple validation
      if (!fullname || !email || !password || !confirmPassword) {
        alert("Please fill in all fields")
        return
      }

      if (password !== confirmPassword) {
        alert("Passwords do not match")
        return
      }

      // Mock signup - in a real app, this would call the Django backend
      mockSignup(fullname, email, password)
    })
  }

  // Mock authentication function
  function mockAuthentication(email, password) {
    // Simulate API call delay
    showLoadingState()

    setTimeout(() => {
      // Store user info in localStorage (for demo purposes only)
      const user = {
        email: email,
        name: email.split("@")[0],
        isAuthenticated: true,
      }

      localStorage.setItem("user", JSON.stringify(user))

      // Redirect to dashboard
      window.location.href = "dashboard.html"
    }, 1000)
  }

  // Mock signup function
  function mockSignup(fullname, email, password) {
    // Simulate API call delay
    showLoadingState()

    setTimeout(() => {
      // In a real app, this would create a user account
      // For demo, just redirect to login page
      alert("Account created successfully! Please login.")
      window.location.href = "login.html"
    }, 1000)
  }

  // Show loading state on button
  function showLoadingState() {
    const submitButton = document.querySelector('button[type="submit"]')
    if (submitButton) {
      submitButton.disabled = true
      submitButton.innerHTML = "Processing..."
    }
  }

  // Check if user is already logged in
  function checkAuthStatus() {
    const user = JSON.parse(localStorage.getItem("user") || "{}")

    // If on auth pages but already logged in, redirect to dashboard
    if (
      (window.location.pathname.includes("login.html") ||
        window.location.pathname.includes("signup.html") ||
        window.location.pathname === "/" ||
        window.location.pathname.includes("index.html")) &&
      user.isAuthenticated
    ) {
      window.location.href = "dashboard.html"
    }

    // If on dashboard but not logged in, redirect to login
    if (window.location.pathname.includes("dashboard.html") && !user.isAuthenticated) {
      window.location.href = "login.html"
    }
  }

  // Check auth status on page load
  checkAuthStatus()
})

