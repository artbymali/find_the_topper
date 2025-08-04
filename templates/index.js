function validateForm() {
    const dept = document.getElementById("dept").value.trim();
    const semester = document.getElementById("semester").value.trim();
    const batch = document.getElementById("batch").value.trim();
    const subject = document.getElementById("subject").value.trim();

    if (!dept || !year || !semester || !batch || !subject) {
      alert("Please fill in all fields.");
      return false;
    }

   

    if (semester < 1 || semester > 8) {
      alert("Semester must be between 1 and 8.");
      return false;
    }

    // All good
    return true;
  }