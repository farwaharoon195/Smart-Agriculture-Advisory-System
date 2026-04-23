async function submitForm(formId, endpoint, resultId, formatter) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const isFileForm = form.enctype === 'multipart/form-data';
    const options = {
      method: 'POST',
      body: isFileForm ? new FormData(form) : new URLSearchParams(new FormData(form)),
    };

    const response = await fetch(endpoint, options);
    const data = await response.json();
    document.getElementById(resultId).innerText = formatter(data);
  });
}

submitForm('crop-form', '/crop', 'crop-result', (d) => `Recommended: ${d.recommended_crops.join(', ')}`);
submitForm('disease-form', '/disease', 'disease-result', (d) => d.disease_result);
submitForm('irrigation-form', '/irrigation', 'irrigation-result', (d) => d.irrigation_advice);
submitForm('market-form', '/market', 'market-result', (d) => d.prediction);
