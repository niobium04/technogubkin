const input = document.getElementById('data-input');
const data = input.value;

function updateDOM(result) {
  document.getElementById('resultOutput').textContent = result;
}

document.getElementById("runCodeButton").addEventListener("click", function() {
    document.getElementById("card1").style.display = "block";
    document.getElementById("card2").style.display = "block";
    document.getElementById("card3").style.display = "block";
    document.getElementById("card4").style.display = "block";
  });

document.addEventListener('click', function(event) {
  var target = event.target;

  if (target.classList.contains('carddd')) {
    target.classList.toggle('open');
  }
});

