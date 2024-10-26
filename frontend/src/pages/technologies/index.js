import { Title, Container, Main } from '../../components'
import styles from './styles.module.css'
import MetaTags from 'react-meta-tags'

const Technologies = () => {
  
  return <Main>
    <MetaTags>
      <title>О проекте</title>
      <meta name="description" content="Фудграм - Технологии" />
      <meta property="og:title" content="О проекте" />
    </MetaTags>
    
    <Container>
      <h1 className={styles.title}>Технологии</h1>
      <div className={styles.content}>
        <div>
          <h2 className={styles.subtitle}>Технологии, которые применены в этом проекте:</h2>
          <div className={styles.text}>
            <ul className={styles.textItem}>
              <li className={styles.textItem}>
                Python 3.10
              </li>
              <li className={styles.textItem}>
                Django 4.2.16
              </li>
              <li className={styles.textItem}>
                Django REST Framework 3.15.2
              </li>
              <li className={styles.textItem}>
                Djoser 2.2.3
              </li>
              <li className={styles.textItem}>
                Gunicorn 20.1.0
              </li>
              <li className={styles.textItem}>
                Docker 27.3.1
              </li>
              <li className={styles.textItem}>
                PostgreSQL 13
              </li>
              <li className={styles.textItem}>
                Nginx
              </li>
              <li className={styles.textItem}>
                Docker Compose
              </li>
              <li className={styles.textItem}>
                Git
              </li>
              <li className={styles.textItem}>
                CI/CD (GitHub Actions)
              </li>
            </ul>
          </div>
        </div>
      </div>
      
    </Container>
  </Main>
}

export default Technologies

