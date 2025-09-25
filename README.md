# Insurance-App
live link : https://insurance-app-by-tejas.streamlit.app/

```mermaid
flowchart TD
    A[Start Application] --> B[Load Model insurance.pkl]
    B --> C{Model Loaded?}
    C -- No --> E[Show Error & Stop]
    C -- Yes --> D[Show Sidebar Navigation]

    D --> F[Home Page]
    D --> G[About Page]
    D --> H[Contact Page]

    F --> I[User Inputs Age, BMI, Smoker Status]
    I --> J[Submit Form]
    J --> K[Pass Data to Model]
    K --> L[Generate Prediction]
    L --> M[Show Result Box with Premium Estimate]

    G --> N[Show Project Info & Model Details]
    H --> O[Show Contact Form]

    M --> P[End]
    N --> P
    O --> P
