using UnityEngine;
using System.Collections;

using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

public class UDPSend : MonoBehaviour
{
    //public static UDP Instance { get; set; }

    private static int localPort;

    [SerializeField] private string IP;
    [SerializeField] public int port;

    IPEndPoint remoteEndPoint;
    UdpClient client;

    string strMessage = "";

    public string textString;

    // call it from shell (as program)
    private static void Main()
    {
        UDPSend sendObj = new UDPSend();
        sendObj.init();

        // testing via console
        // sendObj.inputFromConsole();
    }

    public void Start()
    {
        init();
    }

    void OnGUI()
    {
        Rect rectObj = new Rect(40, 380, 200, 400);
        GUIStyle style = new GUIStyle();
        style.alignment = TextAnchor.UpperLeft;
        GUI.Box(rectObj, "# UDPSend-Data\n" + IP + " " + port + " #\n"
                    + "shell> nc -lu 127.0.0.1  " + port + " \n"
                , style);

        // send message
        strMessage = GUI.TextField(new Rect(40, 450, 140, 20), strMessage);
        if (GUI.Button(new Rect(190, 450, 40, 20), "Send"))
        {
            //sendString(strMessage + "\n");
            setIP(strMessage);
        }
    }

    public void init()
    {
        //print("UDPSend.init()");

        // define properties
        IP = "10.42.1.254";
        //IP = "10.234.2.201";
        port = 5007;

        remoteEndPoint = new IPEndPoint(IPAddress.Parse(IP), port);
        client = new UdpClient();

        //print("Sending to " + IP + " : " + port);
        //print("Testing: nc -lu " + IP + " : " + port);

    }

    private void inputFromConsole()
    {
        try
        {
            string text;
            do
            {
                text = Console.ReadLine();

                if (text != "")
                {

                    byte[] data = Encoding.UTF8.GetBytes(text);

                    client.Send(data, data.Length, remoteEndPoint);
                }
            } while (text != "");
        }
        catch (Exception err)
        {
            print(err.ToString());
        }

    }

    private void setIP(string ip)
    {
        IP = ip;
    }

    // sendData
    public void sendString(string message)
    {
        try
        {
            //if (message != "")
            //{

            byte[] data = Encoding.UTF8.GetBytes(message);

            client.Send(data, data.Length, remoteEndPoint);
            //}
        }
        catch (Exception err)
        {
            print(err.ToString());
        }
    }
}

