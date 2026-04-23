import React, { useEffect, useState } from 'react'
import { getHealth, getCropRecommendation } from '../services/api'
import { translations } from '../i18n/translations'

export function App() {
  const [lang, setLang] = useState('en')
  const [health, setHealth] = useState('loading...')
  const [result, setResult] = useState(null)

  useEffect(() => {
    getHealth().then((d) => setHealth(d.status)).catch(() => setHealth('offline'))
  }, [])

  const t = translations[lang]

  const runRecommendation = async () => {
    const data = await getCropRecommendation({
      district: 'Lahore',
      soil_type: 'loamy',
      season: 'summer',
    })
    setResult(data)
  }

  return (
    <main className="container">
      <h1>{t.title}</h1>
      <p>{t.subtitle}</p>
      <p>API Health: {health}</p>
      <button onClick={() => setLang(lang === 'en' ? 'ur' : 'en')}>Switch EN/UR</button>
      <button onClick={runRecommendation}>{t.crop}</button>
      {result && (
        <section>
          <h3>Recommended</h3>
          <ul>{result.recommended_crops.map((c) => <li key={c}>{c}</li>)}</ul>
        </section>
      )}
    </main>
  )
}
