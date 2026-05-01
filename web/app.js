const form = document.getElementById('mesa-form');
const result = document.getElementById('result');

function toList(text) {
  return text
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean);
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  result.textContent = 'Ejecutando...';

  const payload = {
    prompt: document.getElementById('prompt').value.trim(),
    constraints: toList(document.getElementById('constraints').value),
    preferences: toList(document.getElementById('preferences').value),
    max_generations: Number(document.getElementById('max_generations').value || 2),
  };

  try {
    const response = await fetch('/api/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    result.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    result.textContent = `Error de red: ${error}`;
  }
});
