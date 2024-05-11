#include <gtk/gtkmm.h>

// Function to handle button click event
static void on_button_clicked(GtkWidget *button, gpointer user_data) {
    // Get the entry text
    const gchar *text = gtk_entry_get_text(GTK_ENTRY(user_data));
    
    // Display the text in the console
    GtkTextBuffer *buffer = gtk_text_view_get_buffer(GTK_TEXT_VIEW(user_data));
    gtk_text_buffer_insert_at_cursor(buffer, text, -1);
    gtk_text_buffer_insert_at_cursor(buffer, "\n", -1);
}

int main(int argc, char *argv[]) {
    // Initialize GTK
    gtk_init(&argc, &argv);

    // Create the main window
    GtkWidget *window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(window), "Simple GUI Example");
    gtk_container_set_border_width(GTK_CONTAINER(window), 10);
    gtk_widget_set_size_request(window, 400, 300);
    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);

    // Create a box container
    GtkWidget *box = gtk_box_new(GTK_ORIENTATION_VERTICAL, 5);
    gtk_container_add(GTK_CONTAINER(window), box);

    // Create an entry widget
    GtkWidget *entry = gtk_entry_new();
    gtk_entry_set_placeholder_text(GTK_ENTRY(entry), "Enter command here");
    gtk_box_pack_start(GTK_BOX(box), entry, FALSE, FALSE, 0);

    // Create a scrol
