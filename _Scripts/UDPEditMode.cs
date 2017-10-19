using UnityEngine;
using System.Collections;

using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

[ExecuteInEditMode]
public class UDPEditMode : MonoBehaviour {

    private static int localPort;

    [SerializeField] private string IP;
    [SerializeField] public int port;


    IPEndPoint remoteEndPoint;
    UdpClient client;

    string strMessage = "";

    // call it from shell (as program)
    private static void Main()
    {
        UDPEditMode sendObj = new UDPEditMode();
        sendObj.init();

        // testing via console
        // sendObj.inputFromConsole();
    }

    public void Start()
    {
        init();
    }

    public void init()
    {
        //print("UDP.init()");

        // define properties
        IP = "10.234.2.49";
        port = 5005;

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
        //Try catch doesnt work probably because its being run on edit mode and not play mode. Adding it will print an error.
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
            //print(err.ToString());
        }
    }
}
