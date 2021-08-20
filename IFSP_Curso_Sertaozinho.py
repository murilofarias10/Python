{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "IFSP - Curso Sertaozinho.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "authorship_tag": "ABX9TyOAJ/xbB4DTwS3fOwMhvIgo",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/murilofarias10/AnaliseComPython/blob/main/IFSP_Curso_Sertaozinho.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "0BkyMr3-FhY_"
      },
      "source": [
        "#teste_iniciando"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "BkZ0yrVKbVLu"
      },
      "source": [
        "**Strings**"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "YXKNf39DbjRM"
      },
      "source": [
        "nome = 'aaabbccdd'\n",
        "\n",
        "#nº inicial : ir até : pular\n",
        "print(nome[2:4:2])\n",
        "print(nome[2::4])\n",
        "\n",
        "frase = 'Aprendendo Python'\n",
        "#contando qtde caracteres\n",
        "print(len(frase))\n",
        "#ou\n",
        "contador = len(frase)\n",
        "print(contador)\n",
        "\n",
        "#Utilizando Replace para substituir algo\n",
        "frase = frase.replace('Python', 'Linguagem Python')\n",
        "print(frase)\n",
        "\n",
        "#contando quantos e tem na frase\n",
        "print(frase.count('e'))\n",
        "\n",
        "#localizando onde esta algo\n",
        "print(frase.find('python'))\n",
        "\n",
        "#slit para fazer a divisao\n",
        "print(frase.split())\n",
        "\n",
        "#tudo em maiusculo\n",
        "print(frase.upper())\n",
        "\n",
        "#tudo em minusculo\n",
        "print(frase.lower())\n",
        "\n",
        "#capitalizar, primeira em maiusculo\n",
        "print(frase.capitalize())\n",
        "\n",
        "#primeira letra de cada frase em maiusculo\n",
        "print(frase.title())\n",
        "\n",
        "#o que é maiusculo passa minusculo e vice versa\n",
        "print(frase.swapcase())"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "BfngtbEiDOhG",
        "outputId": "8f685754-be96-4c93-b96b-b4718e5badd8"
      },
      "source": [
        "frase = '     Aprendendo Python '\n",
        "print(frase)\n",
        "#contando caracteres\n",
        "print(len(frase))\n",
        "\n",
        "#removando espaços antes e apos a frase\n",
        "frase = frase.strip()\n",
        "print(len(frase))\n",
        "\n",
        "#removendo espaços a direita\n",
        "frase = '     Aprendendo Python    '\n",
        "print(frase.rstrip())\n",
        "print(len(frase))\n",
        "frase = '     Aprendendo Python    '\n",
        "print(frase.lstrip())\n",
        "print(len(frase))"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "     Aprendendo Python \n",
            "23\n",
            "17\n",
            "     Aprendendo Python\n",
            "26\n",
            "Aprendendo Python    \n",
            "26\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "AxRxg_ebtG23",
        "outputId": "2a6d00aa-22d5-4625-8049-c76a21f720cc"
      },
      "source": [
        "frase = '     Aprendendo Python '\n",
        "print(frase)\n",
        "#contando caracteres\n",
        "print(len(frase))\n",
        "\n",
        "#removando espaços antes e apos a frase\n",
        "frase = frase.strip()\n",
        "print(len(frase))\n",
        "\n",
        "#contatenação\n",
        "nome = 'Maria'\n",
        "sobrenome = 'Silva'\n",
        "nomeCompleto = nome +' ' + sobrenome\n",
        "print(nomeCompleto)\n",
        "\n",
        "#Escapando Caracteres \" ou ' \n",
        "string_frase = '''Ola, testando uma string\n",
        "vou utilizar ' ou\" para o armazenamento'''\n",
        "print(string_frase)\n",
        "cantora = \"A cantona Sinner O' cooner\"\n",
        "print(cantora)\n",
        "curso = 'Tenha bastante atenção ao estudar \"Python\"'\n",
        "print(curso)\n",
        "teste = \"Tenha bastante atenção ao estudar \\\"Python\\\"\" #\\\" Texto\\\"\n",
        "print(teste)\n",
        "barra = \"Escapando com \"\"\\ \"\n",
        "print(barra)"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "     Aprendendo Python \n",
            "23\n",
            "17\n",
            "Maria Silva\n",
            "Ola, testando uma string\n",
            "vou utilizar ' ou\" para o armazenamento\n",
            "A cantona Sinner O' cooner\n",
            "Tenha bastante atenção ao estudar \"Python\"\n",
            "Tenha bastante atenção ao estudar \"Python\"\n",
            "Escapando com \\ \n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "ye9kPLmyvV_k",
        "outputId": "571b5d47-13ca-4424-90b5-e1ffcba78fd3"
      },
      "source": [
        "# %s string | %d inteiro | %f decimal\n",
        "nome = 'Fernando'\n",
        "idade = 27\n",
        "print('O nome informado é: %s' %nome)\n",
        "print ('Com idade de %d anos' %idade)\n",
        "print('o nome informado é: ' + nome + ' e ele possui é: ' + str(idade) + ' anos')\n",
        "print('o nome informado é: ' + nome + ' e ele possui ' + 'idade é: {}'.format(idade) + 'anos')\n",
        "print('o nome informado é: ' + nome + 'e ele possui idade é: ' + format(idade) + 'anos')"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "O nome informado é: Fernando\n",
            "Com idade de 27 anos\n",
            "o nome informado é: Fernando e ele possui é: 27 anos\n",
            "o nome informado é: Fernando e ele possui idade é: 27anos\n",
            "o nome informado é: Fernandoe ele possui idade é: 27anos\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Pern--ocwdRr"
      },
      "source": [
        "raio = 30.46257\n",
        "print('Formatando decimais: %f' %raio)\n",
        "print('Formatando decimais: %.2f' %raio)\n",
        "print('Formatando decimais: %.3f' %raio)"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "7nF6V6Iyxxj6",
        "outputId": "e2f61407-364f-4e13-c1fb-4ee8a740d3cc"
      },
      "source": [
        "#utilizando o r na frente\n",
        "teste = r\"utilizamos \\n \"\n",
        "teste2 = r'utlizamos \"\\n\"'\n",
        "print(teste)\n",
        "print(teste2)"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "utilizamos \\n \n",
            "utlizamos \"\\n\"\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "ax5rOW119Sop",
        "outputId": "74406872-1efe-46c0-be8b-afd9dce20d01"
      },
      "source": [
        "#centralizando e colocando caracteres\n",
        "documento = 'ola meu nome é murilo'\n",
        "print(documento.center(50, \"*\"))\n",
        "#preenchendo somente a direita e a esquerda\n",
        "print(documento.ljust(50, \"*\"))\n",
        "print(documento.rjust(50, \"*\"))"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "**************ola meu nome é murilo***************\n",
            "ola meu nome é murilo*****************************\n",
            "*****************************ola meu nome é murilo\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "GwsXoQ7tAvxX",
        "outputId": "6c7cd553-85ad-4ac6-dc95-9004fccf92ef"
      },
      "source": [
        "#isalnum (ambos), isalpha (somente letra) e isnumeric (somente numero)\n",
        "\n",
        "validacao = 'murilo'\n",
        "valida = '12345'\n",
        "dois = 'Murilo123'\n",
        "\n",
        "print(validacao.isalnum()) #true\n",
        "print(validacao.isalpha()) #true\n",
        "print(validacao.isnumeric()) #false\n",
        "\n",
        "print(valida.isalnum()) #true\n",
        "print(valida.isalpha()) #false\n",
        "print(valida.isnumeric()) # true\n",
        "\n",
        "print(dois.isalnum()) #true\n",
        "print(dois.isalpha()) #false\n",
        "print(dois.isnumeric()) # false"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "True\n",
            "True\n",
            "False\n",
            "True\n",
            "False\n",
            "True\n",
            "True\n",
            "False\n",
            "False\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "3m5nPjKtIUp0"
      },
      "source": [
        "#imprimindo lista com ordem ao contraria\n",
        "mista = ['Murilo', 'Thamie', 'Briane', 15, 18, 'Caio']\n",
        "print(mista)\n",
        "print(mista[-3])\n",
        "\n",
        "#alterar valor\n",
        "\n",
        "mista[3] = 5\n",
        "print(mista)\n",
        "\n",
        "#append para adicionar um item ao final\n",
        "mista.append('Teste')\n",
        "print(mista)\n",
        "\n",
        "#insert insere em alguma posição\n",
        "mista.insert(1, \"Roberto\")\n",
        "print(mista)\n",
        "\n"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "_fqMYlZrLNsA",
        "outputId": "425b8144-553e-4ea8-d5ea-391a7779cfdf"
      },
      "source": [
        "#Função extend unifica as listas\n",
        "mista = ['Murilo', 'Thamie', 'Briane', 15, 18, 'Caio']\n",
        "marte = [1,2,3,4,5]\n",
        "\n",
        "print(mista)\n",
        "print(marte)\n",
        "\n",
        "marte.extend(mista)\n",
        "print(marte)"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "['Murilo', 'Thamie', 'Briane', 15, 18, 'Caio']\n",
            "[1, 2, 3, 4, 5]\n",
            "[1, 2, 3, 4, 5, 'Murilo', 'Thamie', 'Briane', 15, 18, 'Caio']\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "ET_5M9tfNxoN",
        "outputId": "622fbf25-4342-469f-c8b0-a825ea7600b6"
      },
      "source": [
        "#removendo item de uma lista\n",
        "#remove para remover um item especifico\n",
        "print(marte)\n",
        "marte.remove('Briane')\n",
        "print(marte)\n",
        "\n"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "[1, 2, 3, 4, 5, 'Murilo', 'Thamie', 'Briane', 15, 18, 'Caio']\n",
            "[1, 2, 3, 4, 5, 'Murilo', 'Thamie', 15, 18, 'Caio']\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "S8pnqTKOPlcM",
        "outputId": "4af8d43a-cafc-4701-dcfb-90c2eee32fb5"
      },
      "source": [
        "#função POP para remover de um item especifico\n",
        "nova_lista = ['Ronnan', 'Maico', 'Murilo', 'Tiago']\n",
        "print(nova_lista)\n",
        "\n",
        "nova_removido = nova_lista.pop(0)\n",
        "print(nova_removido)  \n",
        "print(nova_removido)"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "['Ronnan', 'Maico', 'Murilo', 'Tiago']\n",
            "Ronnan\n",
            "Ronnan\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "xh18nb0cS-GU",
        "outputId": "ecad47e3-f082-40be-8d4d-75aac17bb521"
      },
      "source": [
        "valor = 'murilo'\n",
        "aluno = 'murilo'\n",
        "frase = 'Aprendendo Python com o IFSP'\n",
        "\n",
        "print(frase[11:17])\n",
        "\n",
        "print(valor.upper())\n",
        "print(len(aluno))"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Python\n",
            "MURILO\n",
            "6\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "DYciOGjAT8jN",
        "outputId": "520f0901-a60c-4a14-99d2-8df78a419917"
      },
      "source": [
        "#forma errada para backup\n",
        "alunos = ['jose', 'joao', 'luiz']\n",
        "alunos_backup = alunos\n",
        "print(alunos_backup)\n",
        "alunos.clear()\n",
        "print('apos o clear {}'.format(alunos_backup))\n",
        "\n",
        "#forma correta | utilizando o copy\n",
        "alunos = ['jose', 'joao', 'luiz']\n",
        "alunos_backup = alunos.copy()\n",
        "print(alunos_backup)\n",
        "alunos.clear()\n",
        "print(alunos_backup)"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "['jose', 'joao', 'luiz']\n",
            "apos o clear []\n",
            "['jose', 'joao', 'luiz']\n",
            "['jose', 'joao', 'luiz']\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "WopECcREiOse"
      },
      "source": [
        "#Faça um programa que pergunta a idade\n",
        "#o peso e a altura e decide se esta APTO a ser do Exercito\n",
        "#Para entrar no exercito é preciso ter mais de 18 pesar mais ou igual 60 Kg e medir mais ou igual 1.7\n",
        "idade = int(input('Qual sua idade ?'))\n",
        "peso = float(input('Qual seu peso ?'))\n",
        "altura = float(input('Qual sua altura'))\n",
        "\n",
        "if idade > 18 and peso >= 60 and altura >=1.7:\n",
        "  print('APTO ao exercito')\n",
        "\n",
        "else:\n",
        "  print('NAO APTO')"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Ezi9zZODWazy"
      },
      "source": [
        "#Faça um programa que leia a quantidade de pessoas que serão convidados para uma festa\n",
        "#Após isso o programa ira pergunta o nome de todos as pessoas e colocar \n",
        "#numa lista de convidados e imprimir todos os nomes da lista\n",
        "pessoas = int(input('Quantidade de pessoas para a festa ?'))\n",
        "contador = pessoas\n",
        "inicial = 0\n",
        "lista_convidados = []\n",
        "\n",
        "while inicial < contador:\n",
        "  convidado = str(input('Digite nome da pessoa:'))\n",
        "  lista_convidados.append(convidado)\n",
        "  inicial = inicial + 1\n",
        "#print('sua lista de convidados é:{}'.format(lista_convidados))\n",
        "\n",
        "for x in lista_convidados:\n",
        "  n= lista_convidados.index(x)+1\n",
        "  print(str(n) + ' Convidado nome:'+ x)\n",
        "  \n",
        "  "
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Acf7_3qSqVA5"
      },
      "source": [
        "#verifique se o nome do usuario começa com M\n",
        "nome = str(input('Digite seu nome'))\n",
        "\n",
        "if nome[0].upper() == 'M':\n",
        "  print('OK')\n",
        "  print('1ª letra digitado: ' + nome[0].upper())\n",
        "else:\n",
        "  print('NOK')\n",
        "\n"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "-4VtORzCnwB1"
      },
      "source": [
        "#Escreva função que recebe objeto de coleção e retorna o valor do maior numero dentro da\n",
        "#coleção e retorna o menor numero\n",
        "print(\"Inicio\")\n",
        "\n",
        "lista = []\n",
        "inicio = 1\n",
        "fim = 4\n",
        "while inicio < fim:\n",
        "  valores = int(input('Digite ' + str(inicio)  + ' numero: \\n'))\n",
        "  print('\\n')\n",
        "  lista.append(valores)\n",
        "  inicio = inicio + 1\n",
        "print('\\n')\n",
        "print('Menor valor digitado é: {}\\n'.format(min(lista)))\n",
        "print('Maior valor digitado é: {}\\n'.format(max(lista)))\n",
        "\n",
        "\n",
        "\n",
        "\n"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "QJyTlik1Cy0L"
      },
      "source": [
        "nome = input('Digite seu nome: ')\n",
        "idade = input('Digite sua idade: ')\n",
        "print('seu nome é ' + nome+ ' sua idade é ' + idade)\n",
        "print('quantidade ' + str(len(nome)) + ' caracteres ')\n",
        "print('Duas primeiras letras é: ' + nome[0:2])"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "-Nz1gF3qEFKE"
      },
      "source": [
        "#Solicite ao usuario informe seu nome\n",
        "#verifique se existe a palavra jose em qualquer parte do nome\n",
        "\n",
        "nome = str(input('Digite seu nome completo'))\n",
        "verificacao = 'JOSE'\n",
        "nome_ver = nome.upper()\n",
        "\n",
        "if nome_ver.find(verificacao, 0) > -1:\n",
        "  print('Seu nome contem: ' + str(verificacao))\n",
        "else:\n",
        "  print('Seu nome não contem: ' + str(verificacao))\n"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "6Q7sYqu4xNvi"
      },
      "source": [
        "#Solicite ao usuario uma frase\n",
        "#motrar frase em minusculo\n",
        "#mostrar frase em maiusculo\n",
        "#contar quantidade de caracteres sem os espaços\n",
        "#contar quantidade de caracteres com os espaços\n",
        "\n",
        "frase = str(input('Digite uma frase'))\n",
        "frase_maiusculo = frase.upper()\n",
        "frase_minusculo = frase.lower()\n",
        "print('\\n')\n",
        "print('frase_minusculo é:' + frase_minusculo)\n",
        "print('\\n')\n",
        "print('frase_maiusculo é:' + frase_maiusculo)\n",
        "\n",
        "frase_sem_espaco = frase.replace(' ', '')\n",
        "\n",
        "com_espaco = (len(frase))\n",
        "conta_caracteres = (len(frase_sem_espaco))\n",
        "print('\\n')\n",
        "print('Total de letras da frase sem espaço: ' + str(conta_caracteres))\n",
        "print('\\n')\n",
        "print('Total de letras da frase com espaço: ' + str(com_espaco))"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Zr7-QVLc32Iq"
      },
      "source": [
        "#PROFESSOR\n",
        "#Solicite ao usuario uma frase\n",
        "#motrar frase em minusculo\n",
        "#mostrar frase em maiusculo\n",
        "#contar quantidade de caracteres sem os espaços\n",
        "#contar quantidade de caracteres com os espaços\n",
        "\n",
        "\n",
        "frase = input('Uma frase')\n",
        "\n",
        "print('frase maisculo: ' + frase.upper())\n",
        "print('frase minusculo: ' + frase.lower())\n",
        "print('qtde total caracteres: ' + str(len(frase)))\n",
        "print('qtde caracteres sem espaço: ' +str(len(frase) - frase.count(' ')))\n",
        "print('qtde espaço: ' + str(frase.count(' ')))\n"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "YsE4vmKhoRlC"
      },
      "source": [
        "# expressão regular https://regex101.com/"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "gQgapgWeBRJe",
        "outputId": "e80d3348-43ab-4c36-ea20-19da2a9dbb8a"
      },
      "source": [
        "#utilização do comando SPLIT\n",
        "#transforma em uma string em uma lista de acordo com os caracteres passados\n",
        "\n",
        "nome = input(\"Digite aqui o seu nome completo: \")\n",
        "teste= nome.split(\"i\")\n",
        "print(teste)\n",
        "print(\"Primeiro nome: \" + teste[0])\n",
        "print(\"Segundo nome: \" + teste[1])"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Digite aqui o seu nome completo: murilo farias\n",
            "['mur', 'lo far', 'as']\n",
            "Primeiro nome: mur\n",
            "Segundo nome: lo far\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "DT4-7lBxOmE7"
      },
      "source": [
        "#Utilizando um API para buscar informações em um site\n",
        "#Importando bibliotecas\n",
        "import requests\n",
        "import json\n",
        "import time\n",
        "import datetime\n",
        "\n",
        "#identificando o site\n",
        "url='https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL'\n",
        "\n",
        "while True:\n",
        "  time.sleep(3)\n",
        "  requisicao = requests.get(url)\n",
        "\n",
        "  cotacao = json.loads(requisicao.text)\n",
        "\n",
        "  print('Moeda: ' + cotacao['USDBRL']['bid'])\n"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "9b7oPagyVO4e"
      },
      "source": [
        "#Utilizando um API para buscar informações em um site\n",
        "#consulta clima tempo #digitando nome da cidade\n",
        "import requests\n",
        "import json\n",
        "import time\n",
        "\n",
        "cidade = str(input('Digite nome da cidade: '))\n",
        "print('\\n')\n",
        "while True:\n",
        "  requisicao = requests.get('https://api.hgbrasil.com/weather?array_limit=2&fields=only_results,temp,'+ str(cidade) +',forecast,max,min,date&key=18420e13')\n",
        "\n",
        "  busca = json.loads(requisicao.text)  \n",
        "  \n",
        "  informacoes = str((busca['forecast']))\n",
        "  \n",
        "  novo = informacoes.split(\",\")\n",
        "\n",
        "  data = novo[0]\n",
        "\n",
        "  \n",
        "  valor_max = novo[1]\n",
        "  valor_min = novo[2]\n",
        "  \n",
        "  data_novo = data.replace(\"[{'date':\", \"\")\n",
        "\n",
        "  novo_valor_max = valor_max.replace(\"'max':\", \"\")\n",
        "  novo_valor_min = valor_min.replace(\"'min':\", \"\")\n",
        "\n",
        "  novo_valor_min_b = novo_valor_min.replace(\"}\", \"\")\n",
        "  data_novo_b = data_novo.replace(\"'\", \"\")\n",
        "\n",
        "  print('Cidade Pesquisada: ' + cidade)\n",
        "  print('Temperatura Atual: ' + str(busca[\"temp\"])) \n",
        "  print('Data de hoje: ' + data_novo_b)\n",
        "  print('Temperatura maxima: ' + novo_valor_max)\n",
        "  print('Temperatura minima: ' + novo_valor_min_b)\n",
        "\n",
        "  time.sleep(10)"
      ],
      "execution_count": null,
      "outputs": []
    }
  ]
}