# Insurance-App



live link : https://insurance-app-by-tejas.streamlit.app/



``` mermaid

graph TD
    A[Start Application] --> B{Load ML Model ('insurance.pkl')};
    B --> C{Model Loaded Successfully?};
    C -- No --> D[Display Error & Stop];
    C -- Yes --> E[Display UI: Sidebar & Main Page];
    
    E --> F{User Selects Page via Sidebar};
    F --> G[Home Page];
    F --> H[About Page];
    F --> I[Contact Page];

    G --> G1[Display Input Form: Age, BMI, Smoker];
    G1 --> G2{User Clicks 'Predict Premium'};
    G2 -- Yes --> G3[Process User Input];
    G3 --> G4[Make Prediction with Model];
    G4 --> G5[Display Estimated Premium];
    G5 --> E;

    H --> H1[Display Project Information];
    H1 --> E;

    I --> I1[Display Contact Form];
    I1 --> I2{User Submits Form};
    I2 -- Yes --> I3[Show Success/Error Message];
    I3 --> E;

```
