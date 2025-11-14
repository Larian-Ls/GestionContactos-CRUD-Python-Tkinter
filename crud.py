# Sistema CRUD simple para gestionar contactos con nombre y teléfono.

import tkinter as tk
import mysql.connector

# Mostrar ventanas de error
def displayError(errorName):
    error = tk.Toplevel()
    error.title("[!]")
    error.geometry("300x200")
    error.resizable(False, False)
    error.config(bg="#333333")

    nameLabel = tk.Label(error, text="[!]:"+errorName, font=("Courier", 12), fg="white", bg="#333333")
    nameLabel.pack()

# Funciones para cada botón
def displayViewContacts():
    conn = None
    try:
        secondaryWindow = tk.Toplevel()
        # secondaryWindow.geometry("300x200")
        secondaryWindow.title("View contacts")
        # secondaryWindow.resizable(False, False)
        secondaryWindow.config(bg="#333333")

        # Entrys y labels
        resultsLabel = tk.Label(secondaryWindow, text="", font=("Courier", 12), fg="white", bg="#333333")
        resultsLabel.config(justify="left")
        resultsLabel.pack()

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="contacts"
        )

        cursor = conn.cursor()

        query = "SELECT * FROM users"
        cursor.execute(query)
        results = cursor.fetchall()

        formatedResults = str(results)

        for c in formatedResults:
            formatedResults = formatedResults.replace("[(", "")
            formatedResults = formatedResults.replace(")]", "")
            formatedResults = formatedResults.replace("'", "")
            formatedResults = formatedResults.replace("('", "")
            formatedResults = formatedResults.replace(" (", "")
            formatedResults = formatedResults.replace("),", "\n")
            formatedResults = formatedResults.replace(",", "\t\t")

        resultsLabel.config(text=formatedResults)

    except mysql.connector.Error:
        displayError("View contacts failed")
    except NameError:
        displayError("Database connection failed")
    finally:
        if conn:
            conn.close()

def displayAddContact():
    def addContact():
        conn = None
        cursor = None
        try:
            name = nameEntry.get()
            tel = int(telEntry.get())
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="contacts"
            )

            cursor = conn.cursor()

            query = "SELECT * FROM users WHERE BINARY name = %s"
            cursor.execute(query, (name,))
            user = cursor.fetchone()

            # Comprobar si el usuario existe
            if user:
                displayError("Contact already exists")
            else:
                query = "INSERT INTO users VALUES(%s, %s)"
                cursor.execute(query, (name, tel))
                conn.commit()
        except mysql.connector.Error:
            displayError("Add contact failed")
        except ValueError:
            displayError("Incorrect values entered")
        finally:
            if conn:
                conn.close()
            secondaryWindow.destroy()            

    secondaryWindow = tk.Toplevel()
    secondaryWindow.geometry("300x200")
    secondaryWindow.title("Add contact")
    secondaryWindow.resizable(False, False)
    secondaryWindow.config(bg="#333333")

    # Entrys y labels
    nameLabel = tk.Label(secondaryWindow, text="NAME:", font=("Courier", 12), fg="white", bg="#333333")
    nameLabel.pack()

    nameEntry = tk.Entry(secondaryWindow, width=20)
    nameEntry.pack()

    telLabel = tk.Label(secondaryWindow, text="TEL:", font=("Courier", 12), fg="white", bg="#333333")
    telLabel.pack()

    telEntry = tk.Entry(secondaryWindow, width=20)
    telEntry.pack()

    add = tk.Button(secondaryWindow, text="ADD CONTACT", width=20, font=("Courier", 12), bg="#90C7FF", command=addContact)
    add.pack(padx=20, pady=15)

def displayUpdateContact():
    def updateContact():
        conn = None
        try:
            name = nameEntry.get()

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="contacts"
            )

            cursor = conn.cursor()

            query = "SELECT * FROM users WHERE BINARY name = %s"
            cursor.execute(query, (name,))
            user = cursor.fetchone()

            # Comprobar si el usuario existe
            if user:
                updtWindow = tk.Toplevel()
                updtWindow.geometry("300x200")
                updtWindow.title("Update contact")
                updtWindow.resizable(False, False)
                updtWindow.config(bg="#333333")                

                def applyUpdate():
                    try:
                        newConn = None
                        newCursor = None
                        newConn = mysql.connector.connect(
                            host="localhost",
                            user="root", 
                            password="root",
                            database="contacts"
                        )
                        updtName = updtNameEntry.get()
                        updtTel= int(updtTelEntry.get())

                        newCursor = newConn.cursor()

                        query = "UPDATE users SET name = %s, tel = %s WHERE name = %s"
                        newCursor.execute(query, (updtName, updtTel, name))
                        newConn.commit()
                    except Exception as e:
                        displayError(f"Update contact failed: " + e)
                    finally:
                        if newConn != None:
                            newConn.close()
                        if newCursor != None:
                            newCursor.close()
                        updtWindow.destroy()
                # Entrys y labels
                titleLabel = tk.Label(updtWindow, text="SET NEW NAME AND\nTELEPHONE NUMBER", font=("Courier", 15, "bold"), fg="white", bg="#333333")
                titleLabel.pack()

                updtNameLabel = tk.Label(updtWindow, text="NAME:", font=("Courier", 12), fg="white", bg="#333333")
                updtNameLabel.pack()

                updtNameEntry = tk.Entry(updtWindow, width=20)
                updtNameEntry.pack()

                updtTelLabel = tk.Label(updtWindow, text="TEL:", font=("Courier", 12), fg="white", bg="#333333")
                updtTelLabel.pack()

                updtTelEntry = tk.Entry(updtWindow, width=20)
                updtTelEntry.pack()

                update = tk.Button(updtWindow, text="UPDATE CONTACT", width=20, font=("Courier", 12), bg="#90C7FF", command=applyUpdate)
                update.pack(padx=20, pady=15)

            else:
                displayError("User not exists")
        except mysql.connector.Error:
            displayError("Update contact failed")
        except ValueError:
            displayError("Incorrect values entered")
        finally:
            if conn != None:
                conn.close()
            secondaryWindow.destroy()

    secondaryWindow = tk.Toplevel()
    secondaryWindow.geometry("300x200")
    secondaryWindow.title("Update contact")
    secondaryWindow.resizable(False, False)
    secondaryWindow.config(bg="#333333")

    # Entrys y labels
    titleLabel = tk.Label(secondaryWindow, text="SELECT A CONTACT", font=("Courier", 15, "bold"), fg="white", bg="#333333")
    titleLabel.pack()

    nameLabel = tk.Label(secondaryWindow, text="NAME:", font=("Courier", 12), fg="white", bg="#333333")
    nameLabel.pack()

    nameEntry = tk.Entry(secondaryWindow, width=20)
    nameEntry.pack()

    update = tk.Button(secondaryWindow, text="UPDATE CONTACT", width=20, font=("Courier", 12), bg="#90C7FF", command=updateContact)
    update.pack(padx=20, pady=15)
    
def displayDeleteContact():
    def deleteContact():
        conn = None
        name = nameEntry.get()

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="contacts"
            )

            cursor = conn.cursor()

            query = "SELECT * FROM users WHERE BINARY name = %s"
            cursor.execute(query, (name,))
            user = cursor.fetchone()

            # Comprobar si el usuario existe
            if user:
                query = "DELETE FROM users WHERE name = %s"
                cursor.execute(query, (name,))
                conn.commit()
            else:
                displayError("Contact not exists")
        except mysql.connector.Error:
            displayError("Delete contact failed")
        except ValueError:
            displayError("Incorrect values entered")
        finally:
            if conn:
                conn.close()
            secondaryWindow.destroy()            

    secondaryWindow = tk.Toplevel()
    secondaryWindow.geometry("300x200")
    secondaryWindow.title("Remove contact")
    secondaryWindow.resizable(False, False)
    secondaryWindow.config(bg="#333333")

    # Entrys y labels
    nameLabel = tk.Label(secondaryWindow, text="NAME:", font=("Courier", 12), fg="white", bg="#333333")
    nameLabel.pack()

    nameEntry = tk.Entry(secondaryWindow, width=20)
    nameEntry.pack()

    delete = tk.Button(secondaryWindow, text="REMOVE CONTACT", width=20, font=("Courier", 12), bg="#90C7FF", command=deleteContact)
    delete.pack(padx=20, pady=15)  

main = tk.Tk()
main.geometry("300x200")
main.config(bg="#333333")
main.title("CRUD system")
main.resizable(False, False)

# Labels
title = tk.Label(text="CONTACT MANAGER", font=("Courier", 20, "bold"), fg="white")
title.config(bg="#333333")
title.pack()

subtitle = tk.Label(text="SELECT AN OPTION:", font=("Courier", 12), fg="white")
subtitle.config(bg="#333333")
subtitle.pack()

# Botones de elección
addButton = tk.Button(text="ADD CONTACT", width=20, font=("Courier", 12), bg="#90C7FF")
addButton.config(command=displayAddContact)
addButton.pack()

viewButton = tk.Button(text="VIEW ALL CONTACTS", width=20, font=("Courier", 12), bg="#90C7FF")
viewButton.config(command=displayViewContacts)
viewButton.pack()

updButton = tk.Button(text="UPDATE CONTACT", width=20, font=("Courier", 12), bg="#90C7FF")
updButton.config(command=displayUpdateContact)
updButton.pack()

remButton = tk.Button(text="REMOVE CONTACT", width=20, font=("Courier", 12), bg="#E23F3F")
remButton.config(command=displayDeleteContact)
remButton.pack()

main.mainloop()