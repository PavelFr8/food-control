document.addEventListener("DOMContentLoaded", () => {
  const selected = document.getElementById("selected-features");
  const available = document.getElementById("available-features");

  document.querySelectorAll(".food-chip").forEach((chip) => {
    const input = chip.querySelector("input");

    if (input.checked) {
      chip.classList.add("selected");
      selected.appendChild(chip);
    } else {
      chip.classList.add("available");
      available.appendChild(chip);
    }

    chip.addEventListener("click", onChipClick);
  });

  function onChipClick(e) {
    e.preventDefault();

    const chip = e.currentTarget;
    const input = chip.querySelector("input");

    if (chip.classList.contains("selected")) {
      chip.classList.remove("selected");
      chip.classList.add("available");
      input.checked = false;
      available.appendChild(chip);
    } else {
      chip.classList.remove("available");
      chip.classList.add("selected");
      input.checked = true;
      selected.appendChild(chip);
    }
  }

  document.querySelectorAll(".food-chip").forEach((chip) => {
    chip.addEventListener("click", onChipClick);
  });
});
