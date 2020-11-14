package worker;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.exceptions.JedisConnectionException;

import java.sql.*;
import org.json.JSONObject;

class Worker {

  private static String POSTGRES_HOST = System.getenv("POSTGRES_HOST");

  private static String POSTGRES_DATABASE = System.getenv("POSTGRES_DATABASE");

  private static String POSTGRES_PASSWORD = System.getenv("POSTGRES_PASSWORD");

  private static String POSTGRES_PORT = System.getenv("POSTGRES_PORT");

  private static String POSTGRES_USER = System.getenv("POSTGRES_USER");

  private static String REDIS_HOST = System.getenv("REDIS_HOST");

  private static String REDIS_PASSWORD = System.getenv("REDIS_PASSWORD");

  private static String REDIS_PORT = System.getenv("REDIS_PORT");

  public static void main(String[] args) {
    try {

      String URL_Redis = strConnectionRedis();

      Jedis redis = connectToRedis(new Jedis(URL_Redis));

      String ping = redisPing(redis);

      System.out.println(ping);

      Connection dbConn = connectToDB();

      System.err.println("Watching vote queue");

      while (true) {
        String voteJSON = redis.blpop(0, "votes").get(1);
        JSONObject voteData = new JSONObject(voteJSON);
        String voterID = voteData.getString("voter_id");
        String vote = voteData.getString("vote");

        System.err.printf("Processing vote for '%s' by '%s'\n", vote, voterID);
        updateVote(dbConn, voterID, vote);
      }
    } catch (SQLException e) {
      e.printStackTrace();
      System.exit(1);
    }
  }

  static void updateVote(Connection dbConn, String voterID, String vote) throws SQLException {
    PreparedStatement insert = dbConn.prepareStatement("INSERT INTO votes (id, vote) VALUES (?, ?)");
    insert.setString(1, voterID);
    insert.setString(2, vote);

    try {
      insert.executeUpdate();
    } catch (SQLException e) {
      PreparedStatement update = dbConn.prepareStatement("UPDATE votes SET vote = ? WHERE id = ?");
      update.setString(1, vote);
      update.setString(2, voterID);
      update.executeUpdate();
    }
  }

  static String redisPing(Jedis conn) {
    return "Server is runing:" + conn.ping();
  }

  public static String strConnectionRedis() {
    return "redis://default:" + REDIS_PASSWORD + "@" + REDIS_HOST + ":" + REDIS_PORT;
  }

  static Jedis connectToRedis(Jedis conn) {
    while (true) {
      try {
        conn.keys("*");
        break;
      } catch (JedisConnectionException e) {
        System.err.println("Waiting for redis");
        sleep(1000);
      }
    }

    System.err.println("Connected to redis");
    return conn;
  }

  static Connection connectToDB() throws SQLException {

    Connection conn = null;

    try {

      Class.forName("org.postgresql.Driver");

      String url = strConnectionPostgres();

      while (conn == null) {
        try {
          conn = DriverManager.getConnection(url);
        } catch (SQLException e) {
          System.err.println("Waiting for db");
          sleep(1000);
        }
      }

      PreparedStatement st = conn.prepareStatement(
          "CREATE TABLE IF NOT EXISTS votes (id VARCHAR(255) NOT NULL UNIQUE, vote VARCHAR(255) NOT NULL)");
      st.executeUpdate();

    } catch (ClassNotFoundException e) {
      e.printStackTrace();
      System.exit(1);
    }

    System.err.println("Connected to db");
    return conn;
  }

  public static String strConnectionPostgres() {
    return "jdbc:postgresql://" + POSTGRES_HOST + ":" + POSTGRES_PORT + "/" + POSTGRES_DATABASE + "?user=" + POSTGRES_USER + "&password="
        + POSTGRES_PASSWORD + "&ssl=true&sslfactory=org.postgresql.ssl.NonValidatingFactory";
  }

  static void sleep(long duration) {
    try {
      Thread.sleep(duration);
    } catch (InterruptedException e) {
      System.exit(1);
    }
  }
}
