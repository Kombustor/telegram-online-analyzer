from utils.database import Database
import pandas as pd
import matplotlib.pyplot as plt


def main():
    db = Database('./config.ini')

    analyze_status_distribution(db)


def analyze_status_distribution(db):
    # Select data from database
    query = "SELECT status,COUNT(*) as count FROM {table} GROUP BY status ORDER BY status DESC;"\
        .format(table=db.table_name)
    df = pd.read_sql(query, db.connection)

    # No data = unknown, unprecise = recently, precise = offline/online
    total_count = df.sum()['count']

    # Derive counts for every value
    unknown_count = df.loc[df['status'] == 'unknown']['count'][0]
    unprecise_count = df.loc[df['status'] == 'recently']['count'][1]
    precise_count = df.loc[df['status'].isin(['offline', 'online'])].sum()['count']

    # Create dataframe with every derived count
    deriv_df = pd.DataFrame({
        'share': [unknown_count, unprecise_count, precise_count]
    }, index=['unknown', 'unprecise', 'precise'])
    # Data transformation into percentage shares
    deriv_df['share'] = deriv_df['share'].apply(lambda x: x / total_count)

    # Drawing plot
    deriv_df.plot(kind='pie', y='share', autopct='%1.1f%%')
    plt.show()


if __name__ == '__main__':
    main()
