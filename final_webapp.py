import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Main page content
def main_page():
    st.title("Main Page - Shulue Jiang")
    
    # General guide on how to use the app
    st.write("""
    ## How to Use This Webapp
    """)
    
    # Navigation guide
    st.write("""
    ### Navigation
    - **Main Page:** General usage guide.
    - **Project Overview:** Goals, findings, and methodology.
    - **Data Sources:** Information on data origins.
    - **Interactive App:** Direct interaction with data filters and results.
    """)
    
    # Description of the Interactive App
    st.write("""
    ### Interactive App
    - This is where you can interact with the data by applying various filters and viewing the results.
    - In the Interactive App page, you can use the sidebar to select different filters such as neighborhood, address, price range, year built, and square footage.
    - Detailed notes appear if only one property matches the filters, providing insights into risk factors and other relevant indices that affect insurance premiums.
    - You can also view correlation graphs that illustrate the relationship between insurance premiums and various indices.
    """)
    
    # Explanation on understanding plots/charts
    st.write("""
    ### Understanding Plots/Charts
    - The correlation graphs on the Interactive App page help you understand how different factors (like price, square footage, or neighborhood risk indices) correlate with estimated insurance premiums.
    - A positive correlation indicates that as one variable increases, the other tends to increase as well, which helps in assessing the impact of various factors on insurance costs.
    """)
    
    # Major Gotchas
    st.write("""
    ## Major Gotchas
    - Technical Limitations: Some features may not work as expected. For instance, text search in filters can be case-sensitive or might not handle special characters gracefully.
    
    - Data Reliability: Since the calculations for insurance premiums are based on modeled data and assumptions (like multiplication factors for various indices), the estimates may not perfectly align with actual premiums provided by insurance companies.
    
    - User Interface: While functional, the user interface may lack some refinements, particularly in terms of layout and responsiveness on different devices or screens.
    """)


# Project overview page content
def project_overview():
    st.title("Project Overview")
    
    # Introduction to the project's goals
    st.write("""
    ### What did you set out to study?  
    My goal is to estimate the annual insurance premiums for all properties listed on the Bay Area Modern website. Data 1 contains specific details of all properties on the site, including footage, year of built, and price. Data 2 provides details from about 1,000 fire emergency records, from which I calculated the frequency of fires in different neighborhoods. Data 3 lists various crimes in different neighborhoods over the past month. I first categorized the crimes into high, medium, and low risk, then calculated the frequency of each crime level in different neighborhoods. 
    
    Ultimately, I used the number of standard deviations from the mean to calculate various indices. My initial insurance premium was set at $1,244, which is also the average annual premium in the San Francisco area for 2023. Based on my personal experience, I multiplied the fire index by 50, the high-risk index by 50, the medium-risk index by 30, the low-risk index by 10, the construction age index by 100, the room area index by 100, and the price index by 100 to determine the final estimated premium.
            
    I hope that through my model, customers planning to buy properties on the Bay Area Modern website can have a better understanding of potential insurance costs. During this process, they can also learn about the frequency of fires and the frequency of different types of crime in the property's area.         
    """)

    # Discoveries from the project
    st.write("""
    ### What did you Discover?
    My final output estimates the annual insurance premiums for all properties listed on the Bay Area Modern website, along with recent fire frequency and crime rates of different types in the last month in the property's area. 
    
    I also included correlation analysis graphs of all indices I used with the premiums, allowing users to visually understand the impact of each variable on the final result during my model building process.
    """)

    # Challenges faced during the project
    st.write("""
    ### What difficulties did you have in completing the project?
    Different insurance companies may vary in how they adjust premiums based on different indices. This is internal information for insurance companies, so it is not easily obtainable. Therefore, I need to use my own settings to predict the final premiums.
    
    Also, one of the main challenges was dealing with incomplete or inconsistent data, which required robust preprocessing to ensure accuracy in the analysis. Additionally, integrating user input for real-time data filtering in the Streamlit app presented technical difficulties, particularly in ensuring that the app remains responsive and intuitive.
    """)

    # Skills desired during the project
    st.write("""
    ### What skills did you wish you had while you were doing the project?
    As a beginner in coding, throughout the project, a deeper knowledge of advanced data cleaning techniques and a better understanding of interactive web frameworks like Streamlit would have been beneficial. Skills in user experience design could also have enhanced the development of the tool, making it more accessible and easier to use.
    """)

    # Future expansions of the project
    st.write("""
    ### What would you do “next” to expand or augment the project?
    By using more data and information, the changes in premiums based on different indices can be made more precise. For example, I could use the specific amounts from fire insurance claims from some companies to infer how fires affect premiums. Additionally, I could include some potential factors that might change the premiums, making this model more comprehensive.
    """)


# Data sources page content
def data_sources():
    st.title("Data Sources")
    st.write("""
    ### Data Source 1
    **URL for Website**: [Bay Area Modern Real Estate](https://www.bayareamodern.com/san-francisco-real-estate/?pg=1)
    
    **Brief Description**:
    It is a listing on Bay Area Modern, featuring homes for sale in San Francisco. This platform offers an extensive database of real estate properties, including features like average days on market, average price per square foot, and median listing price. Users can search for properties by various criteria, view detailed listings with photos, and get real-time alerts on new listings. This site is a resource for both buyers and sellers, providing insights into the San Francisco real estate market.

    ### Data Source 2
    **URL for API**: [Fire Incidents Data](https://data.sfgov.org/Public-Safety/Fire-Incidents/wr8u-xric/about_data)
    
    **Brief Description**:
    This dataset provides a comprehensive record of fire incidents that the San Francisco Fire Department responded to. It includes details such as the incident number, address, type of each unit responding, call type, actions taken, and property loss.

    ### Data Source 3
    **URL for Website**: [Civic Hub Crime Data](https://www.civichub.us/ca/san-francisco/gov/police-department/crime-data/neighborhoods)
    
    **Brief Description**:
    It leads to a dataset from Civic Hub that provides detailed crime data for San Francisco, organized by neighborhood. This data includes crime rates and interactive maps for each neighborhood, allowing users to visualize and compare crime statistics across different areas of the city.
    """)

# Main interactive app page content with updated code
def interactive_app():
    @st.cache
    def load_data():
        df = pd.read_csv('final_result.csv')
        df['Price'] = df['Price'].replace('[\$,]', '', regex=True).astype(float)
        df['Premium'] = df['Premium'].replace('[\$,]', '', regex=True).astype(float)
        df['Year_built'] = pd.to_numeric(df['Year_built'], errors='coerce')
        df['Sq_ft'] = pd.to_numeric(df['Sq_ft'], errors='coerce')
        df.replace('None', np.nan, inplace=True)
        return df

    df = load_data()

    st.sidebar.header('Filters')

    neighborhoods = df['Neighborhood'].dropna().unique()
    all_neighborhoods = ['all'] + list(neighborhoods)
    selected_neighborhoods = st.sidebar.multiselect('Select Neighborhood:', options=all_neighborhoods, default='all')

    st.sidebar.markdown("""
    #### Enter Address:
    *This is the best way to obtain the Estimated Premium since the notes will only be displayed when there is only one property on the page*
    """)
    input_address = st.sidebar.text_input('')

    price_range = st.sidebar.slider('Select Price Range:', min_value=0, max_value=int(df['Price'].max()), value=(0, int(df['Price'].max())), format="%d", step=10000)

    year_built_range = st.sidebar.slider('Select Year Built Range:', min_value=int(df['Year_built'].min()), max_value=int(df['Year_built'].max()), value=(int(df['Year_built'].min()), int(df['Year_built'].max())))

    sq_ft_range = st.sidebar.slider('Select Square Feet Range:', min_value=0, max_value=int(df['Sq_ft'].max()), value=(0, int(df['Sq_ft'].max())), format="%d", step=100)

    if st.sidebar.button('Apply Filters'):
        if 'all' in selected_neighborhoods:
            filtered_data = df.copy()
        else:
            filtered_data = df[df['Neighborhood'].isin(selected_neighborhoods)]
        
        if input_address:
            filtered_data = filtered_data[filtered_data['Address'].str.contains(input_address, case=False, na=False)]

        filtered_data = filtered_data[(filtered_data['Price'] >= price_range[0]) & (filtered_data['Price'] <= price_range[1])]
        filtered_data = filtered_data[(filtered_data['Year_built'] >= year_built_range[0]) & (filtered_data['Year_built'] <= year_built_range[1])]
        filtered_data = filtered_data[(filtered_data['Sq_ft'] >= sq_ft_range[0]) & (filtered_data['Sq_ft'] <= sq_ft_range[1])]
        
        st.write(filtered_data)

        if len(filtered_data) == 1:
            st.write("Notes:")
            st.write("High risk events includes Homicide, Robbery, Arson, Assault, Sex Offender, Weapons Offer, Kidnapping.")
            st.write("Medium risk events includes Burglary, Drug Offense, Drug Violation, Embezzlement, Forgery And Counterfeiting, Fraud, Motor Vehicle Theft, Promotion, Stolen Property, Weapons Carriage Etc, Vandalism, Traffic Violation Arrest, Larceny Theft.")
            st.write("Low risk events includes Case Closure, Courtesy Report, Disorderly Conduct, Fire Report, Liquor Laws, Lost Property, Malicious Mischief, Miscellaneous Investment, Missing Person, Non-Critical, Offenses Against The Family And Children, Other Miscellaneous, Recovered Vehicle, Suicide, Suspicious Occ, Traffic Collision, Vehicle Impounded, Warrant.")
            st.write("The higher the Fire_index value, the higher the frequency of occurrence in the past 1000 fire alarm records in the San Francisco area.")
            
            index_columns = ['Price_index', 'Sq_ft_index', 'Year_built_index', 'Fire_index', 'High_risk_index', 'Medium_risk_index', 'Low_risk_index']
            high_indexes = [col for col in index_columns if filtered_data.iloc[0][col] > 1]
            if high_indexes:
                st.write(f"Be aware of the '{', '.join(high_indexes)}' because of the high index(es), which will cause significant impact on estimating premium.")
            
            cols_to_check = df.columns.drop('Beds')
            missing_values = [col for col in cols_to_check if pd.isna(filtered_data.iloc[0][col]) or filtered_data.iloc[0][col] == 0]
            if missing_values:
                st.write(f"Be aware of and look up manually the following missing value(s): '{', '.join(missing_values)}'.")

    if st.sidebar.button('Reset Filters'):
        st.experimental_rerun()

    if st.sidebar.button('Show Correlation Graphs'):
        st.markdown("### Correlation Graphs")
        st.markdown("""
        **Note:**
        Take 'Premium' and 'Price_index' as an example. A high positive correlation between 'Premium' and 'Price_index' would suggest that as property prices increase, so do the premiums, which could be intuitive if premiums are based on property values.
        """)
        index_columns = ['Price_index', 'Sq_ft_index', 'Year_built_index', 'Fire_index', 'High_risk_index', 'Medium_risk_index', 'Low_risk_index']
        
        for col in index_columns:
            fig, ax = plt.subplots()
            sns.scatterplot(data=df, x='Premium', y=col, ax=ax, alpha=0.5)
            ax.set_title(f'Correlation between Premium and {col}')
            ax.set_xlabel('Premium')
            ax.set_ylabel(col)
            
            corr_value = df['Premium'].corr(df[col])
            st.write(f'Correlation coefficient between Premium and {col}: {corr_value:.2f}')
            
            st.pyplot(fig)

    else:
        st.write(df)

# Page navigation
page_names_to_funcs = {
    "Main Page": main_page,
    "Project Overview": project_overview,
    "Data Sources": data_sources,
    "Interactive App": interactive_app,
}

st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Select Page:", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

