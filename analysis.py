import psycopg2
import pandas as pd
from datetime import datetime, timedelta
import os
from urllib.parse import urlparse

# def get_db_conn():
#     return psycopg2.connect(
#         host="localhost",
#         database="musictrend",
#         user="postgres",
#         password="Tushar@1745"  # 🔐 Use env var in production
#     )

def get_db_conn():
    url = urlparse(os.environ.get("DATABASE_URL"))

    return psycopg2.connect(
        database=url.path[1:],  # Remove leading /
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

def get_trending_songs(tenant_id):
    conn = get_db_conn()
    last_week = datetime.now() - timedelta(days=7)
    try:
        query = """
    SELECT title, artist, genre, score
    FROM "Song"
    WHERE title IS NOT NULL AND artist IS NOT NULL
    AND "fetchedAt" >= %s
    AND "tenantId" = %s
    ORDER BY score DESC
"""

        df = pd.read_sql(query, conn, params=(last_week, tenant_id))
        return df.to_dict(orient='records')
    finally:
        conn.close()

def get_trending_artists(tenant_id, limit=10):
    conn = get_db_conn()
    last_week = datetime.now() - timedelta(days=7)
    try:
        query = '''
    SELECT artist, COUNT(*) AS song_count,
           SUM(COALESCE(score, 0)) AS total_score,
           AVG(COALESCE(score, 0)) AS avg_score
    FROM "Song"
    WHERE artist IS NOT NULL AND artist != 'Unknown'
    AND "fetchedAt" >= %s
    AND "tenantId" = %s
    GROUP BY artist
    ORDER BY total_score DESC
    LIMIT %s
'''

        df = pd.read_sql(query, conn, params=(last_week, tenant_id, limit))
        return df.to_dict(orient="records")
    finally:
        conn.close()

def get_weekly_report(user_id):
    songs = get_trending_songs(user_id)
    artists = get_trending_artists(user_id, limit=5)
    print("weekly songs are", songs)
    print("weekly artistst are", artists)
    return {
        "top_songs": songs[:5],
        "top_artists": artists
    }


def get_genre_movement(tenant_id):
    conn = get_db_conn()
    now = datetime.now()
    one_week_ago = now - timedelta(days=7)
    two_weeks_ago = now - timedelta(days=14)
    try:
        query = """
        SELECT genre,
               COUNT(*) FILTER (WHERE "fetchedAt" >= %s) AS last_week_count,
               COUNT(*) FILTER (WHERE "fetchedAt" < %s AND "fetchedAt" >= %s) AS prev_week_count
        FROM "Song"
        WHERE genre IS NOT NULL AND genre != ''
        AND "tenantId" = %s

        GROUP BY genre
        ORDER BY last_week_count DESC
        """
        df = pd.read_sql(query, conn, params=(one_week_ago, one_week_ago, two_weeks_ago, tenant_id))
        return df.to_dict(orient='records')
    finally:
        conn.close()

def export_songs_as(tenant_id, format='json'):
    songs = get_trending_songs(tenant_id)
    df = pd.DataFrame(songs)
    if format == 'csv':
        return df.to_csv(index=False)
    return df.to_dict(orient='records')
