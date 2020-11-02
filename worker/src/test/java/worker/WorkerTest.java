package worker;

import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class WorkerTest {
    @Test
    public void updateVote() {
        assertTrue(true);
    }

    @Test
    public void validateConnectionUrl(){
        String connection = Worker.getConnectionUrl("localhost");
        assertEquals("jdbc:postgresql://localhost/postgres", connection);
    }

}